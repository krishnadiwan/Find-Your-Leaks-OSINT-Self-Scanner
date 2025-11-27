# File: scanner/username_check.py
import requests
import streamlit as st
from requests.exceptions import RequestException

# --- Social platforms to check ---
PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Medium": "https://medium.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Discord": "https://discord.com/users/{}",
    "Ko-fi": "https://ko-fi.com/{}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
    "GitLab": "https://gitlab.com/{}"
}

# --- Keywords for not found ---
NOT_FOUND_KEYWORDS = [
    "not found", "doesn't exist", "does not exist", "page not found", "no such user"
]

def check_username(username: str) -> dict:
    """
    Check username existence across social platforms.
    Returns {platform: profile_url} only if found.
    """
    found_sites = {}
    st.write(f"🔍 Checking username `{username}` across {len(PLATFORMS)} platforms...")
    progress = st.progress(0)
    total = len(PLATFORMS)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for i, (platform, url_pattern) in enumerate(PLATFORMS.items(), start=1):
        profile_url = url_pattern.format(username)
        try:
            resp = requests.get(profile_url, headers=headers, timeout=5)
            text = resp.text.lower()
            if resp.status_code == 200 and not any(kw in text for kw in NOT_FOUND_KEYWORDS):
                st.write(f"✅ {platform}: Found → [{profile_url}]({profile_url})")
                found_sites[platform] = profile_url
            else:
                st.write(f"❌ {platform}: Not Found")
        except RequestException:
            st.write(f"⚠️ {platform}: Could not connect")

        progress.progress(i / total)

    st.success("Username scan completed ✅")
    return found_sites


# --- Streamlit UI for testing ---
def main():
    st.title("Username Checker – Social Media OSINT")
    username = st.text_input("Enter username:")
    if username:
        results = check_username(username)
        if results:
            st.write("### Found Profiles:")
            for platform, link in results.items():
                st.markdown(f"- [{platform}]({link})")
        else:
            st.warning("No profiles found for this username.")

if __name__ == "__main__":
    main()
