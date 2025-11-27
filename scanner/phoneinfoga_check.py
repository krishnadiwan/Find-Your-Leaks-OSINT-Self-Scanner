# File: scanner/phoneinfoga_check.py

import subprocess

def run_phoneinfoga_scan(phone_number, binary_path=None):
    try:
        if not binary_path:
            binary_path = '/home/kali/phoneinfoga'  # path to your PhoneInfoga executable

        result = subprocess.run(
            [binary_path, 'scan', '-n', phone_number],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {"error": result.stderr.strip()}

        # Return as plain text (Streamlit can display in st.text_area or st.code)
        return {"raw_output": result.stdout.strip()}

    except Exception as e:
        return {"error": str(e)}



