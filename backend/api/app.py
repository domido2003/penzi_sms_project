from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import re

app = Flask(__name__)
# CORS(app) 
CORS(app, resources={r"/*": {"origins": [
"http://localhost:3003",
"http://127.0.0.1:3003",
]}})

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="domido2003",
    database="penzi_dating"
)

@app.route('/')
def home():
    return "✅ Penzi Dating API is running"

@app.route('/messages', methods=['POST'])
def handle_message():
    data = request.get_json()
    message_from = data.get('message_from')
    message_to = data.get('message_to')
    content = data.get('content').strip()
    direction = data.get('direction')

    cursor = db.cursor() 

    # 1. Save message
    cursor.execute("""
        INSERT INTO messages (message_from, message_to, content, direction, date_created)
        VALUES (%s, %s, %s, %s, NOW())
    """, (message_from, message_to, content, direction))
    db.commit()

    # 2. Process different message types
    # -- START registration
    if content.lower().startswith("start#"):
        parts = content.split("#")
        if len(parts) == 6:
            _, full_name, age, gender, county, town = parts
            try:
                cursor.execute("""
                    INSERT INTO users (full_name, phone_number, age, gender, county, town)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (full_name, message_from, int(age), gender, county, town))
                db.commit()
            except:
                pass

    # -- DETAILS update
    elif content.lower().startswith("details#"):
        parts = content.split("#")
        if len(parts) == 6:
            edu, job, marital, religion, tribe = parts[1:]
            cursor.execute("""
                UPDATE users SET education_level=%s, profession=%s, marital_status=%s,
                religion=%s, ethnicity=%s WHERE phone_number=%s
            """, (edu, job, marital, religion, tribe, message_from))
            db.commit()

    # -- MYSELF self-description
    elif content.lower().startswith("myself"):
        desc = content[6:].strip()
        cursor.execute("UPDATE users SET self_description=%s WHERE phone_number=%s", (desc, message_from))
        db.commit()

    # -- MATCH request
    elif content.lower().startswith("match#"):
        parts = content.split("#")
        if len(parts) == 3:
            age_range, town = parts[1], parts[2]
            if "-" in age_range:
                min_age, max_age = map(int, age_range.split("-"))
                cursor.execute("SELECT gender FROM users WHERE phone_number=%s", (message_from,))
                sender = cursor.fetchone()
                if sender:
                    gender = sender[0]
                    target_gender = "Female" if gender.lower() == "male" else "Male"
                    cursor.execute("""
                        SELECT full_name, age, phone_number FROM users
                        WHERE gender=%s AND town=%s AND age BETWEEN %s AND %s
                    """, (target_gender, town, min_age, max_age))
                    matches = cursor.fetchall()

                    # Track in match_sessions
                    cursor.execute("""
                        INSERT INTO match_sessions (phone_number, match_criteria_age_min,
                        match_criteria_age_max, town)
                        VALUES (%s, %s, %s, %s)
                    """, (message_from, min_age, max_age, town))
                    db.commit()

                    for match in matches[:3]:
                        name, age, phone = match
                        match_msg = f"{name} aged {age}, {phone}"
                        cursor.execute("""
                            INSERT INTO messages (message_from, message_to, content, direction, date_created)
                            VALUES ('22141', %s, %s, 'OUTGOING', NOW())
                        """, (message_from, match_msg))

                    # Pagination note
                    if len(matches) > 3:
                        cursor.execute("""
                            INSERT INTO match_tracking (phone_number, seen_count) VALUES (%s, 3)
                            ON DUPLICATE KEY UPDATE seen_count = 3
                        """, (message_from,))
                        cursor.execute("""
                            INSERT INTO messages (message_from, message_to, content, direction, date_created)
                            VALUES ('22141', %s, %s, 'OUTGOING', NOW())
                        """, (message_from, "Send NEXT to see more matches."))
                    db.commit()

    # -- NEXT pagination
    elif content.upper() == "NEXT":
        cursor.execute("SELECT gender FROM users WHERE phone_number=%s", (message_from,))
        sender = cursor.fetchone()
        if sender:
            gender = sender[0]
            target_gender = "Female" if gender.lower() == "male" else "Male"

            cursor.execute("SELECT seen_count FROM match_tracking WHERE phone_number=%s", (message_from,))
            result = cursor.fetchone()
            offset = result[0] if result else 3

            cursor.execute("""
                SELECT full_name, age, phone_number FROM users
                WHERE gender=%s AND phone_number != %s LIMIT 3 OFFSET %s
            """, (target_gender, message_from, offset))
            matches = cursor.fetchall()

            if matches:
                for match in matches:
                    name, age, phone = match
                    match_msg = f"{name} aged {age}, {phone}"
                    cursor.execute("""
                        INSERT INTO messages (message_from, message_to, content, direction, date_created)
                        VALUES ('22141', %s, %s, 'OUTGOING', NOW())
                    """, (message_from, match_msg))

                cursor.execute("""
                    UPDATE match_tracking SET seen_count = seen_count + 3 WHERE phone_number = %s
                """, (message_from,))
                db.commit()

    # -- Phone number only (to get profile)
    elif re.match(r"^07\d{8}$", content):
        target = content
        cursor.execute("""
            SELECT full_name, age, county, town, education_level, profession,
                   marital_status, religion, ethnicity FROM users WHERE phone_number=%s
        """, (target,))
        result = cursor.fetchone()
        if result:
            name, age, county, town, edu, job, status, religion, tribe = result
            profile = f"{name} aged {age}, {county}, {town}, {edu}, {job}, {status}, {religion}, {tribe}. " \
                      f"Send DESCRIBE {target} to get more info."
            cursor.execute("""
                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                VALUES ('22141', %s, %s, 'OUTGOING', NOW())
            """, (message_from, profile))
            db.commit()

    # -- DESCRIBE command
    elif content.upper().startswith("DESCRIBE "):
        phone = content.split()[1]
        cursor.execute("""
            SELECT self_description, full_name, age, county, town FROM users WHERE phone_number=%s
        """, (phone,))
        target = cursor.fetchone()
        if target:
            desc, name, age, county, town = target
            msg = f"{name} describes themselves as: {desc}"
            cursor.execute("""
                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                VALUES ('22141', %s, %s, 'OUTGOING', NOW())
            """, (message_from, msg))

            # notify target
            cursor.execute("""
                SELECT full_name, age, county, town FROM users WHERE phone_number=%s
            """, (message_from,))
            requester = cursor.fetchone()
            if requester:
                rname, rage, rcounty, rtown = requester
                notify = f"Hi {name}, {rname} (age {rage}, {rcounty}, {rtown}) is interested in you. " \
                         "Reply YES to know more."
                cursor.execute("""
                    INSERT INTO messages (message_from, message_to, content, direction, date_created)
                    VALUES ('22141', %s, %s, 'OUTGOING', NOW())
                """, (phone, notify))
            db.commit()

    # -- YES message
    elif content.upper() == "YES":
        # Who requested?
        cursor.execute("""
            SELECT message_from FROM messages WHERE message_to=%s AND content LIKE %s
            ORDER BY date_created DESC LIMIT 1
        """, (message_from, "%Reply YES to know more.%"))
        requester = cursor.fetchone()
        if requester:
            rphone = requester[0]
            cursor.execute("""
                SELECT full_name, age, county, town, education_level, profession,
                       marital_status, religion, ethnicity, self_description
                FROM users WHERE phone_number=%s
            """, (message_from,))
            u = cursor.fetchone()
            if u:
                name, age, county, town, edu, job, status, religion, tribe, desc = u
                full = f"{name}, aged {age}, {county}, {town}, {edu}, {job}, {status}, {religion}, {tribe}."
                if desc:
                    full += f" Description: {desc}"
                cursor.execute("""
                    INSERT INTO messages (message_from, message_to, content, direction, date_created)
                    VALUES ('22141', %s, %s, 'OUTGOING', NOW())
                """, (rphone, full))
                db.commit()

    cursor.close()
    return jsonify({"status": "✅ Message saved and processed"})

if __name__ == '__main__':
    app.run(debug=True)
