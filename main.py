import json
from datetime import datetime


def lambda_handler(event, context):
    # Example usage:
    json_data = [
        {"type": "START", "id": "ABC123", "timestamp": "1681722000", "comments": "No issues - brand new and shiny!"},
        {"type": "END", "id": "ABC123", "timestamp": "1681743600", "comments": "Car is missing both front wheels!"},
        {"type": "START", "id": "ABC456", "timestamp": "1680343200", "comments": "Small dent on passenger door"},
        {"type": "END", "id": "ABC456", "timestamp": "1680382800", "comments": ""}
    ]
    parse_json_and_generate_summary(json_data)
    summary_records = parse_json_and_generate_summary(json_data)
    print(summary_records)


def parse_json_and_generate_summary(json_data):
    sessions = {}

    for entry in json_data:
        session_id = entry.get("id")
        if session_id:
            if session_id not in sessions:
                sessions[session_id] = {"type": None, "start_timestamp": None, "end_timestamp": None, "comments": None}

            if entry["type"] == "START":
                sessions[session_id]["type"] = "START"
                sessions[session_id]["start_timestamp"] = entry["timestamp"]
                sessions[session_id]["comments"] = entry["comments"]
            elif entry["type"] == "END":
                sessions[session_id]["type"] = "END"
                sessions[session_id]["end_timestamp"] = entry["timestamp"]
                if sessions[session_id]["start_timestamp"]:
                    input_epoch = int(sessions[session_id]["start_timestamp"]) - int(
                        sessions[session_id]["end_timestamp"])
                if sessions[session_id]["comments"] == '':
                    damage = False
                else:
                    damage = True
                d = datetime.utcfromtimestamp(3600 * ((input_epoch + 1800) // 3600))
                h = d.hour + (d.minute + 30 + (d.second + 30) / 60) / 60

    summary_records = []

    for session_id, session_data in sessions.items():
        summary_records.append({
            "id": session_id,
            "duration": int(session_data["start_timestamp"]) + int(session_data["end_timestamp"]),
            "start_timestamp": session_data["start_timestamp"],
            "end_timestamp": session_data["end_timestamp"],
            "damage": damage,
            "returnLater": int(h)
        })

    return summary_records

