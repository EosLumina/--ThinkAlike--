def ethical_matching(user_profile, potential_matches):
    safe_matches = []
    for match in potential_matches:
        if not is_high_risk_combination(user_profile, match):
            safe_matches.append(match)
    return safe_matches

def is_high_risk_combination(user1, user2):
    # Example: Avoid matching users with mutually reinforcing risks
    if user1.behavioral_flags.get("gambling") and user2.behavioral_flags.get("gambling"):
        return True
    if user1.behavioral_flags.get("suicidal") and user2.behavioral_flags.get("suicidal"):
        return True
    return False
