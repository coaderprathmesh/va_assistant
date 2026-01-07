from flask import Blueprint, request, jsonify, render_template
import sqlite3
import pandas as pd
import io
from db_path import database_path
upload_bp = Blueprint("upload_csv", __name__)

def upsert_volunteer(record, cursor):
    """Insert or update a single volunteer record."""
    cursor.execute("""
        INSERT INTO volunteers (
            submission_id, name, email, phone, current_place_of_residence,
            my_skillset, field_1c8f11d, form_name_id, created_at, user_id,
            user_agent, user_ip, referrer
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(submission_id) DO UPDATE SET
            name = excluded.name,
            email = excluded.email,
            phone = excluded.phone,
            current_place_of_residence = excluded.current_place_of_residence,
            my_skillset = excluded.my_skillset,
            field_1c8f11d = excluded.field_1c8f11d,
            form_name_id = excluded.form_name_id,
            created_at = excluded.created_at,
            user_id = excluded.user_id,
            user_agent = excluded.user_agent,
            user_ip = excluded.user_ip,
            referrer = excluded.referrer;
    """, (
        record.get("submission_id"),
        record.get("name"),
        record.get("email"),
        record.get("phone"),
        record.get("current_place_of_residence"),
        record.get("my_skillset"),
        record.get("field_1c8f11d"),
        record.get("form_name_id"),
        record.get("created_at"),
        record.get("user_id"),
        record.get("user_agent"),
        record.get("user_ip"),
        record.get("referrer")
    ))

@upload_bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Read CSV directly into pandas DataFrame
    try:
        df = pd.read_csv(io.StringIO(file.stream.read().decode("utf-8")))
    except Exception as e:
        return jsonify({"error": f"CSV read error: {str(e)}"}), 400

    # Normalize column names
    df.columns = [
        "name", "email", "phone", "current_place_of_residence", "my_skillset",
        "field_1c8f11d", "form_name_id", "submission_id", "created_at",
        "user_id", "user_agent", "user_ip", "referrer"
    ]

    # Connect to DB
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Process each row (row by row)
    for _, row in df.iterrows():
        upsert_volunteer(row, cursor)

    conn.commit()
    conn.close()

    return jsonify({"message": f"{len(df)} record(s) inserted or updated successfully."}), 200







