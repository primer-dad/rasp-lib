import re


def analyze_request(data_sources, security_checks):
    for source_key, value_str in data_sources:
        for attack_name, pattern in security_checks:
            match = pattern.search(value_str)
            if match:
                return {
                    "blocked": True,
                    "attack_type": attack_name,
                    "matched_pattern": match.group(0),
                    "source_key": source_key,
                    "input_snip": value_str[:100],
                }
    return {"blocked": False}
