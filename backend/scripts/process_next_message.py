import mysql.connector

# 1. Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="domido2003",
    database="penzi_dating"
)

cursor = connection.cursor()

# 2. Get the latest 'NEXT' message
cursor.execute("""
    SELECT id, message_from, content FROM messages
    WHERE direction = 'INCOMING' AND content = 'NEXT'
    ORDER BY date_created DESC
    LIMIT 1
""")

message = cursor.fetchone()

if message:
    msg_id, sender, content = message
    print(f"📨 Received message: {content}")

    # Get requester's gender to filter opposite gender
    cursor.execute("SELECT gender FROM users WHERE phone_number = %s", (sender,))
    result = cursor.fetchone()

    if result:
        requester_gender = result[0]
        opposite_gender = 'Female' if requester_gender.lower() == 'male' else 'Male'

        # Get how many matches they've already seen
        cursor.execute("SELECT seen_count FROM match_tracking WHERE phone_number = %s", (sender,))
        track = cursor.fetchone()
        offset = track[0] if track else 3

        # Fetch next 3 matches
        cursor.execute("""
            SELECT full_name, age, phone_number FROM users
            WHERE gender = %s AND phone_number != %s
            LIMIT 3 OFFSET %s
        """, (opposite_gender, sender, offset))

        matches = cursor.fetchall()

        if matches:
            # Update match tracking
            if track:
                cursor.execute("UPDATE match_tracking SET seen_count = seen_count + 3 WHERE phone_number = %s", (sender,))
            else:
                cursor.execute("INSERT INTO match_tracking (phone_number, seen_count) VALUES (%s, 6)", (sender,))
            connection.commit()

            # Send match details to user
            for match in matches:
                name, age, phone = match
                match_message = f"{name} aged {age}, {phone}."
                cursor.execute("""
                    INSERT INTO messages (message_from, message_to, content, direction, date_created)
                    VALUES (%s, %s, %s, 'OUTGOING', NOW())
                """, ('22141', sender, match_message))

            # Add final instruction message
            instruction = (
                "Send the number of someone you're interested in to get their full profile. "
                "E.g., 0702556677. To see more matches, reply with NEXT."
            )
            cursor.execute("""
                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                VALUES (%s, %s, %s, 'OUTGOING', NOW())
            """, ('22141', sender, instruction))

            connection.commit()

        else:
            # No more matches available
            cursor.execute("""
                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                VALUES (%s, %s, %s, 'OUTGOING', NOW())
            """, ('22141', sender, "No more matches available at the moment."))
            connection.commit()

    else:
        print("⚠️ Requester's gender not found in the users table.")
else:
    print("❌ No new 'NEXT' message found.")

# 3. Close the connection
cursor.close()
connection.close()
