import json
from flask import request, jsonify
from .patterns import SECURITY_CHECKS


def rasp_check_and_block(logger=None, app_title="RASP"):
    data_sources = []

    if request.values:
        data_sources.extend(request.values.items())

    if request.is_json:
        try:
            data_sources.append(("JSON_PAYLOAD", str(request.get_json())))
        except Exception:
            pass

    for source_key, source_value in data_sources:
        value_str = str(source_value)

        for attack_name, pattern in SECURITY_CHECKS:
            match = pattern.search(value_str)
            if match:
                matched_pattern = match.group(0)

                log_entry = {
                    "message": "RASP: Security Incident Blocked",
                    "attack_type": attack_name,
                    "matched_pattern_snip": matched_pattern,
                    "source_input_key": source_key,
                    "request_uri": request.path,
                    "request_method": request.method,
                    "client_ip": request.remote_addr,
                    "input_value_snip": value_str[:100],
                }

                if logger:
                    logger.log_text(json.dumps(log_entry), severity="WARNING")

                print(json.dumps(log_entry))

                return jsonify({
                    "status": "blocked",
                    "attack_type": attack_name,
                    "matched_string": matched_pattern,
                    "message": "Blocked by RASP middleware",
                }), 403

    return None
