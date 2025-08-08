import mysql.connector

# Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="domido2003",
    database="penzi_dating"
)

cursor = connection.cursor()

# 1. Fetch the latest YES message
cursor.execute("""
    SELECT id, message_from FROM messages
    WHERE direction = 'INCOMING' AND content = 'YES'
    ORDER BY date_created DESC
    LIMIT 1
""")

yes_msg = cursor.fetchone()

if yes_msg:
    msg_id, responder_phone = yes_msg
    print(f"📨 YES reply received from: {responder_phone}")

    # 2. Find the last interest prompt sent TO this responder
    cursor.execute("""
        SELECT message_from FROM messages
        WHERE direction = 'OUTGOING'
        AND content LIKE %s
        AND message_to = %s
        ORDER BY date_created DESC
        LIMIT 1
    """, ("%Do you want to know more about%", responder_phone))

    result = cursor.fetchone()

    if result:
        requester_phone = result[0]
        print(f"🙋 Found interested user: {requester_phone}")

        # 3. Get full profile of the interested person
        cursor.execute("""
            SELECT full_name, age, county, town, education_level, profession,
                   marital_status, religion, ethnicity, self_description
            FROM users
            WHERE phone_number = %s
        """, (requester_phone,))
        
        user = cursor.fetchone()

        if user:
            (name, age, county, town, edu, job, status, religion, tribe, desc) = user

            profile_message = (
                f"{name}, aged {age}, {county} County, {town} town, {edu}, {job}, "
                f"{status}, {religion}, {tribe}. "
            )
            if desc:
                profile_message += f"Self-description: {desc}"

            # 4. Send the profile to the responder (who replied YES)
            cursor.execute("""
                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                VALUES (%s, %s, %s, 'OUTGOING', NOW())
            """, ('22141', responder_phone, profile_message))

            connection.commit()
            print(f"✅ Sent profile of {requester_phone} to {responder_phone}")
        else:
            print("❌ Requester profile not found in users table.")
    else:
        print("⚠️ No matching interest message found for this YES reply.")
else:
    print("❌ No new YES message found.")

# Close DB connection
cursor.close()
connection.close()
