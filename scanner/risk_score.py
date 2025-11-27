# File: scanner/risk_score.py

def calculate_score(
    email_breaches: int,
    username_found_count: int,
    metadata_sensitive: bool,
    total_username_sites: int = 15
) -> tuple[float, str, dict]:
    """
    Calculate a privacy risk score out of 10 with clear percentage contributions.

    Weights (points out of 10):
      - Email breaches: max 4 points
      - Username found: max 3 points
      - Metadata sensitive: max 3 points

    Returns:
      - total_score (float): risk score out of 10
      - level (str): Low / Medium / High
      - breakdown (dict): individual component scores with percentages (as strings with %)
    """
    # --- Weights ---
    max_email = 4
    max_username = 3
    max_metadata = 3

    # --- Email score ---
    email_score = min(email_breaches, max_email)
    email_pct = f"{round((email_score / max_email) * 100, 1)}%"

    # --- Username score ---
    username_percentage = username_found_count / total_username_sites
    username_score = round(username_percentage * max_username, 1)
    username_pct = f"{round(username_percentage * 100, 1)}%"

    # --- Metadata score ---
    metadata_score = max_metadata if metadata_sensitive else 0
    metadata_pct = "100%" if metadata_sensitive else "0%"

    # --- Total score ---
    total_score = round(email_score + username_score + metadata_score, 1)

    # --- Risk level ---
    if total_score >= 7:
        level = "High 🔴"
    elif total_score >= 4:
        level = "Medium 🟡"
    else:
        level = "Low 🟢"

    # ✅ Fixed dictionary syntax
    breakdown = {
        "Email Breaches": {"score": email_score, "pct": email_pct},
        "Username Presence": {"score": username_score, "pct": username_pct},
        "Metadata Sensitive": {"score": metadata_score, "pct": metadata_pct}
    }

    return total_score, level, breakdown


# --- Professional Console Output (Optional) ---
def display_risk_score(score, level, breakdown):
    print("=" * 50)
    print("🔒 PRIVACY RISK SCORE REPORT 🔒")
    print("=" * 50)
    print(f"Total Risk Score : {score}/10")
    print(f"Risk Level       : {level}")
    print("-" * 50)
    print("Breakdown:")
    for k, v in breakdown.items():
        # convert pct string back to number for bar length
        pct_number = float(v['pct'].replace('%', ''))
        bar_length = int(pct_number // 2)  # 50 chars max
        bar = "█" * bar_length + "-" * (50 - bar_length)
        print(f"{k:<20} : {v['score']} points | {v['pct']}")
        print(f"[{bar}]")
    print("=" * 50)


# --- Example usage ---
if __name__ == "__main__":
    score, level, details = calculate_score(
        email_breaches=9,
        username_found_count=9,
        metadata_sensitive=True
    )
    display_risk_score(score, level, details)
