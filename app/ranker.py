# Calculate ATS compatibility
def calculate_ats_compatibility(parsed_data: dict) -> int:

    score = 0
    total_checks = 3

    # Contact info
    if parsed_data.get("has_contact_info"):
        score += 1

    # Education section
    if parsed_data.get("education"):
        score += 1

    # Experience section
    exp_len = len(parsed_data.get("experience", []))
    proj_len = len(parsed_data.get("projects", []))
    if exp_len or proj_len:

        score += min((exp_len + proj_len) / 5, 1)

    ats_percentage = round((score / total_checks) * 100)
    return ats_percentage


