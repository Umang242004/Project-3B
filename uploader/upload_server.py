from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import base64
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def schedule_reels():
    data = request.get_json()
    videos = data["videos"]

    base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    schedule_times = [9, 12, 15, 18, 21]
    result = []

    for i, video in enumerate(videos):
        day_offset = i // 5
        time_index = i % 5
        scheduled_time = base_date + timedelta(days=day_offset, hours=(schedule_times[time_index] - 9))

        # Simulated Upload Process (mocked)
        result.append({
            "filename": video["filename"],
            "scheduled_time": scheduled_time.strftime("%Y-%m-%d %H:%M"),
            "status": "Scheduled ✅"
        })

    return jsonify(result), 200
