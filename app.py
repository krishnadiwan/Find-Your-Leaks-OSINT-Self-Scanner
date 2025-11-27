# File: app.py

import streamlit as st
from scanner.email_check import check_email_breach
from scanner.metadata_check import extract_metadata
from scanner.risk_score import calculate_score
from utils.pdf_generator import generate_report
from scanner.phoneinfoga_check import run_phoneinfoga_scan
from scanner.username_check import check_username  # Custom username checker

# --- Streamlit Page Config ---
st.set_page_config(page_title="Find Your Leaks – OSINT Self-Scanner", layout="centered")
st.title("Find Your Leaks – OSINT Self-Scanner")

# ============================
# PHONEINFOGA SCAN
# ============================
if "phone_info_result" not in st.session_state:
    st.session_state.phone_info_result = {}

phone_number = st.text_input("Enter phone number")
if st.button("Scan Phone Number") and phone_number:
    st.session_state.phone_info_result = run_phoneinfoga_scan(phone_number)

if st.session_state.phone_info_result:
    info = st.session_state.phone_info_result
    if "error" in info:
        st.error(info["error"])
    else:
        st.code(info.get("raw_output", ""))

# ============================
# EMAIL BREACH CHECK
# ============================
if "email_found" not in st.session_state:
    st.session_state.email_found = False
if "breach_count" not in st.session_state:
    st.session_state.breach_count = 0

email = st.text_input("Enter your Email", key="email_input")
if st.button("Check Email Breach") and email:
    check_email_breach(email)
    st.info("HIBP opened in a new tab. Check breaches and come back here.")

breach_confirmed = st.radio(
    "Did Have I Been Pwned show breaches for this email?",
    ("No", "Yes")
)

if breach_confirmed == "Yes":
    st.session_state.email_found = True
    st.session_state.breach_count = st.number_input(
        "Enter the number of data breaches shown on HIBP:",
        min_value=1,
        max_value=100,
        step=1,
        value=1,
        help="Look at the top of the HIBP page — this is the number of breaches for your email."
    )
else:
    st.session_state.email_found = False
    st.session_state.breach_count = 0

if st.session_state.email_found:
    st.success(f"Email found in {st.session_state.breach_count} breaches.")
else:
    st.info("No known breaches found for this email.")

# ============================
# USERNAME CHECK (Custom)
# ============================
if "found_sites" not in st.session_state:
    st.session_state.found_sites = {}

st.subheader("Username OSINT Lookup")
username = st.text_input("Enter a username to scan:")

if st.button("Search Username") and username.strip():
    with st.spinner(f"Searching {username} across platforms..."):
        found_sites = check_username(username)
        st.session_state.found_sites = found_sites

    if found_sites:
        st.success(f"Found {len(found_sites)} accounts:")
        for platform, url in found_sites.items():
            st.markdown(f"- **{platform}** → [Visit Profile]({url})")
    else:
        st.info("No accounts found with this username.")

# ============================
# METADATA CHECK
# ============================
uploaded_file = st.file_uploader("Upload an image (JPG or PNG)")

metadata_sensitive = False
metadata_tags = None

if uploaded_file:
    st.subheader("Metadata Analysis")
    metadata_tags = extract_metadata(uploaded_file)
    if metadata_tags:
        st.write(metadata_tags)
        if any("GPS" in str(tag) or "Model" in str(tag) for tag in metadata_tags):
            metadata_sensitive = True
            st.error("Sensitive metadata detected (GPS/Device info).")
        else:
            st.success("No sensitive metadata found.")
    else:
        st.info("No metadata found in the image.")

# ============================
# PRIVACY RISK SCORE & REPORT
# ============================
if st.button("Calculate Privacy Risk Score"):
    # calculate using actual counts
    score, level, breakdown = calculate_score(
        email_breaches=st.session_state.breach_count,
        username_found_count=len(st.session_state.found_sites),
        metadata_sensitive=metadata_sensitive
    )

    # display score
    st.metric("Privacy Risk Score", f"{score}/10")
    st.write(f"Risk Level: {level}")

    st.write("Score Breakdown:")
    for key, val in breakdown.items():
        st.write(f"- {key.replace('_', ' ').title()}: {val}")

    # generate PDF report
    report_file = generate_report(
        email=email,
        username=username,
        breach_count=st.session_state.breach_count,
        found_sites=st.session_state.found_sites,
        score=score,
        metadata_tags=metadata_tags,
        phone_info=st.session_state.phone_info_result
    )

    # download PDF
    try:
        with open(report_file, "rb") as file:
            st.download_button(
                label="Download Professional PDF Report",
                data=file,
                file_name="FindYourLeaks_Report.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"Failed to load PDF: {e}")
