from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from analysis import (
    get_trending_songs,
    get_trending_artists,
    get_weekly_report,
    get_genre_movement,
    export_songs_as
)
import traceback

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "🎵 Trend Analysis Microservice Running"

@app.route("/trending-songs", methods=["POST"])
def trending_songs():
    data = request.get_json()
    tenant_id = data.get("tenantId")
    if not tenant_id:
        return jsonify({"error": "Missing tenantId"}), 400
    result = get_trending_songs(tenant_id)
    return jsonify(result)

@app.route("/trending-artists", methods=["POST"])
def trending_artists():
    data = request.get_json()
    tenant_id = data.get("tenantId")
    if not tenant_id:
        return jsonify({"error": "Missing tenantId"}), 400
    result = get_trending_artists(tenant_id)
    return jsonify(result)

@app.route("/weekly-report", methods=["POST"])
def weekly_report():
    data = request.get_json()
    print("📥 Received data:", data)

    user_id = data.get("tenantId")
    if not user_id:
        return jsonify({"error": "Missing tenantId"}), 400

    try:
        user_id = str(user_id)
        report = get_weekly_report(user_id)
        print("📊 Generated report:", report)
        return jsonify(report)
    except Exception as e:
        print(f"💥 Exception: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@app.route("/genre-movement", methods=["POST"])
def genre_movement():
    data = request.get_json()
    tenant_id = str(data.get("tenantId"))
    if not tenant_id:
        return jsonify({"error": "Missing tenantId"}), 400

    try:
        movement = get_genre_movement(tenant_id)
        return jsonify(movement)
    except Exception as e:
        print(f"💥 Genre movement error: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@app.route("/export", methods=["POST"])
def export():
    data = request.get_json()
    tenant_id = data.get("tenantId")
    export_format = data.get("format", "json")  # "json" or "csv"
    if not tenant_id:
        return jsonify({"error": "Missing tenantId"}), 400

    if export_format == "csv":
        csv_data = export_songs_as(tenant_id, format="csv")
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=songs.csv"}
        )
    else:
        json_data = export_songs_as(tenant_id, format="json")
        return jsonify(json_data)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
