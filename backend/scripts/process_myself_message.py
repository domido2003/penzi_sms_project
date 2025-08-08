import mysql.connector

# 1. Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="domido2003",
    database="penzi_dating"
)

cursor = connection.cursor()

# 2. Get the latest 'MYSELF' incoming message
cursor.execute("""
    SELECT id, message_from, content FROM messages
    WHERE direction = 'INCOMING' AND content LIKE 'MYSELF%'
    ORDER BY date_created DESC
    LIMIT 1
""")

message = cursor.fetchone()

if message:
    msg_id, sender, content = message
    print(f"📨 Received message: {content}")

    # Remove the word 'MYSELF' and strip any surrounding whitespace
    description = content[6:].strip()

    if description:
        try:
            # Update the user's self-description
            cursor.execute("""
                UPDATE users
                SET self_description = %s
                WHERE phone_number = %s
            """, (description, sender))

            connection.commit()

            if cursor.rowcount > 0:
                print(f"✅ Self-description added for {sender}")

                # Send confirmation + match instructions
                cursor.execute("""
                    INSERT INTO messages (message_from, message_to, content, direction, date_created)
                    VALUES (%s, %s, %s, 'OUTGOING', NOW())
                """, (
                    '22141',
                    sender,
                    "Your profile has been updated successfully. You are now fully registered for dating. "
                    "To find a MPENZI, SMS match#ageRange#town to 22141. For example, match#25-30#Nairobi"
                ))

                connection.commit()
            else:
                print("⚠️ No matching user found for this MYSELF message.")
                cursor.execute("""
                    INSERT INTO messages (message_from, message_to, content, direction, date_created)
                    VALUES (%s, %s, %s, 'OUTGOING', NOW())
                """, (
                    '22141',
                    sender,
                    "We could not find your account to update the profile. Please register first using start#..."
                ))
                connection.commit()

        except mysql.connector.Error as err:
            print("❌ Error while updating self-description:", err)

    else:
        print("⚠️ Message does not contain any description.")
        cursor.execute("""
            INSERT INTO messages (message_from, message_to, content, direction, date_created)
            VALUES (%s, %s, %s, 'OUTGOING', NOW())
        """, (
            '22141',
            sender,
            "Please include a description after the word MYSELF. Example: MYSELF kind, honest, and caring."
        ))
        connection.commit()

else:
    print("❌ No new 'MYSELF' message found.")

# 3. Close the database connection
cursor.close()
connection.close()
