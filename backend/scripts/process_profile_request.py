import mysql.connector

# 1. Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="domido2003",
    database="penzi_dating"
)

cursor = connection.cursor()

# 2. Get the latest message that looks like a phone number
cursor.execute("""
    SELECT id, message_from, content FROM messages
    WHERE direction = 'INCOMING'
    AND content REGEXP '^07[0-9]{8}$'
    ORDER BY date_created DESC
    LIMIT 1
""")

message = cursor.fetchone()

if message:
    msg_id, sender, target_phone = message
    print(f"📨 Request received for: {target_phone}")

    # Look up the profile of the person being requested
    cursor.execute("""
        SELECT full_name, age, county, town, education_level, profession, marital_status, religion, ethnicity
        FROM users
        WHERE phone_number = %s
    """, (target_phone,))

    profile = cursor.fetchone()

    if profile:
        full_name, age, county, town, education, profession, marital, religion, tribe = profile

        details_message = (
            f"{full_name} aged {age}, {county} County, {town} town, {education}, {profession}, "
            f"{marital}, {religion}, {tribe}. Send DESCRIBE {target_phone} to get more details about {full_name}."
        )

        # Send profile info to requester
        cursor.execute("""
            INSERT INTO messages (message_from, message_to, content, direction, date_created)
            VALUES (%s, %s, %s, 'OUTGOING', NOW())
        """, ('22141', sender, details_message))

        # Notify the person whose profile was requested
        cursor.execute("""
            SELECT full_name, age, county, town FROM users WHERE phone_number = %s
        """, (sender,))
        requester = cursor.fetchone()

        if requester:
            r_name, r_age, r_county, r_town = requester
            notify_message = (
                f"Hi {full_name}, a user named {r_name} is interested in you and requested your details. "
                f"They are aged {r_age} based in {r_county}. Do you want to know more about them? Send YES to 22141."
            )

            cursor.execute("""
                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                VALUES (%s, %s, %s, 'OUTGOING', NOW())
            """, ('22141', target_phone, notify_message))

        connection.commit()
    else:
        # User not found
        cursor.execute("""
            INSERT INTO messages (message_from, message_to, content, direction, date_created)
            VALUES (%s, %s, %s, 'OUTGOING', NOW())
        """, ('22141', sender, "No user found with that number."))
        connection.commit()
else:
    print("❌ No new number message found.")

# 3. Close the connection
cursor.close()
connection.close()
