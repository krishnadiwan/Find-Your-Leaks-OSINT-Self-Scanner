import webbrowser

def check_email_breach(email):
    """
    Opens Have I Been Pwned page for the email and returns OSINT links.
    """
    # Open the HIBP page in browser
    url = f"https://haveibeenpwned.com/account/{email}"
    webbrowser.open(url)
    
    # Prepare OSINT links
    links = {
        "Have I Been Pwned": url,
    }
    
    # Return a tuple so your Streamlit app can unpack it
    return True, links


