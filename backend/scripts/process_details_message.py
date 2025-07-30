import mysql.connector

# 1. Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="domido2003",
    database="penzi_dating"
)

cursor = connection.cursor()

# 2. Get the latest 'details#' incoming message
cursor.execute("""
    SELECT id, message_from, content FROM messages
    WHERE direction = 'INCOMING' AND content LIKE 'details#%'
    ORDER BY date_created DESC
    LIMIT 1
""")

message = cursor.fetchone()

if message:
    msg_id, sender, content = message
    print(f"Received message: {content}")

    parts = content.strip().split("#")

    if len(parts) == 6:
        education_level = parts[1].strip()
        profession = parts[2].strip()
        marital_status = parts[3].strip()
        religion = parts[4].strip()
        ethnicity = parts[5].strip()

        try:
            # 3. Update the user's profile
            cursor.execute("""
                UPDATE users
                SET education_level = %s,
                    profession = %s,
                    marital_status = %s,
                    religion = %s,
                    ethnicity = %s
                WHERE phone_number = %s
            """, (education_level, profession, marital_status, religion, ethnicity, sender))
            connection.commit()

            if cursor.rowcount > 0:
                print(f"✅ User profile updated for {sender}")

                # 4. Send system reply message
                cursor.execute("""
                    INSERT INTO messages (message_from, message_to, content, direction, date_created)
                    VALUES (%s, %s, %s, 'OUTGOING', NOW())
                """, (
                    '22141',  # Shortcode
                    sender,
                    "Your profile has been updated successfully. This is the last stage of registration. SMS a brief description of yourself to 22141 starting with the word MYSELF."
                ))
                connection.commit()

            else:
                print("⚠️ No matching user found in the users table.")

        except mysql.connector.Error as err:
            print("❌ Error while updating user:", err)

    else:
        print("❌ Incorrect message format. Use: details#edu#job#marital#religion#tribe")

else:
    print("📭 No new 'details#' message found.")

# 5. Close DB connection
cursor.close()
connection.close()
