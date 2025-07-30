import mysql.connector

# 1. Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="domido2003",
    database="penzi_dating"
)

cursor = connection.cursor()

# 2. Get the latest DESCRIBE message
cursor.execute("""
    SELECT id, message_from, content FROM messages
    WHERE direction = 'INCOMING' AND content LIKE 'DESCRIBE %'
    ORDER BY date_created DESC
    LIMIT 1
""")

message = cursor.fetchone()

if message:
    msg_id, requester, content = message
    print(f"📨 Received message: {content}")

    parts = content.strip().split()
    
    if len(parts) == 2:
        target_number = parts[1].strip()

        # Fetch the self-description of the target user
        cursor.execute("""
            SELECT self_description, full_name, age, county, town, education_level, profession,
                   marital_status, religion, ethnicity
            FROM users WHERE phone_number = %s
        """, (target_number,))
        target_user = cursor.fetchone()

        if target_user:
            (description, name, age, county, town, edu, prof,
             marital, religion, tribe) = target_user

            # 3. Send self-description to the requester
            reply = f"{name} describes themselves as: {description}"
            cursor.execute("""
                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                VALUES (%s, %s, %s, 'OUTGOING', NOW())
            """, ('22141', requester, reply))

            # 4. Notify the target user someone is interested in them
            # First, get requester's details
            cursor.execute("""
                SELECT full_name, age, county, town FROM users WHERE phone_number = %s
            """, (requester,))
            requester_data = cursor.fetchone()

            if requester_data:
                req_name, req_age, req_county, req_town = requester_data

                notify_msg = (
                    f"Hi {name}, a person called {req_name} is interested in you "
                    f"and requested your details. He is aged {req_age} and based in {req_county}, {req_town}.\n"
                    "Do you want to know more about him? Reply with YES to 22141."
                )

                cursor.execute("""
                    INSERT INTO messages (message_from, message_to, content, direction, date_created)
                    VALUES (%s, %s, %s, 'OUTGOING', NOW())
                """, ('22141', target_number, notify_msg))

            connection.commit()
            print("✅ Self-description and interest alert sent.")
        else:
            print("❌ Target user not found.")
    else:
        print("❌ Invalid DESCRIBE format. Use: DESCRIBE 07XXXXXXXX")
else:
    print("❌ No new DESCRIBE message found.")

# 5. Close connection
cursor.close()
connection.close()
