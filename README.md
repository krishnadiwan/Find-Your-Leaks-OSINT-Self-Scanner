🔍 Find Your Leaks — OSINT Self-Scanner
Kali Linux Installation Guide (with PhoneInfoga + Streamlit App)

This guide explains how to install PhoneInfoga, clone the OSINT Self-Scanner repository, set up a Python virtual environment, install dependencies, and run the Streamlit app on Kali Linux.

📦 Requirements

Kali Linux (or any Debian-based Linux)

Python 3.8+

pip3

git

curl

Internet connection

🛠 Step 1 — Install PhoneInfoga

Run the official installer script:

bash <( curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install )


Install PhoneInfoga into /usr/local/bin:

sudo install ./phoneinfoga /usr/local/bin/phoneinfoga


Verify installation:

./phoneinfoga version

📥 Step 2 — Clone the OSINT Self-Scanner Repository
git clone https://github.com/krishnadiwan/Find-Your-Leaks-OSINT-Self-Scanner.git
cd Find-Your-Leaks-OSINT-Self-Scanner

🐍 Step 3 — Create & Activate Python Virtual Environment
python3 -m venv myenv
source myenv/bin/activate

📚 Step 4 — Install Required Python Packages

IMPORTANT: You wrote requiremetnts.txt — ensure the file is actually named
requirements.txt or change the command accordingly.

pip3 install -r requirements.txt

▶️ Step 5 — Run the Streamlit App
streamlit run app.py
