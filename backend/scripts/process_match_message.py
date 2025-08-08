import mysql.connector

# 1. Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="domido2003",
    database="penzi_dating"
)

cursor = connection.cursor()

# 2. Get the latest 'match#' incoming message
cursor.execute("""
    SELECT id, message_from, content FROM messages
    WHERE direction = 'INCOMING' AND content LIKE 'match#%'
    ORDER BY date_created DESC
    LIMIT 1
""")

message = cursor.fetchone()

if message:
    msg_id, sender, content = message
    print(f"📨 Received match request: {content}")

    # Split and validate the message
    parts = content.strip().split("#")
    if len(parts) == 2:
        age_range_town = parts[1].strip().split("#")
        if len(age_range_town) == 2:
            age_range = age_range_town[0]
            town = age_range_town[1].strip()

            if "-" in age_range:
                min_age, max_age = age_range.split("-")
                try:
                    min_age = int(min_age)
                    max_age = int(max_age)

                    # 3. Get the sender's gender
                    cursor.execute("SELECT gender FROM users WHERE phone_number = %s", (sender,))
                    user_info = cursor.fetchone()

                    if user_info:
                        sender_gender = user_info[0]
                        opposite_gender = "Female" if sender_gender.lower() == "male" else "Male"

                        # 4. Find all matching users
                        cursor.execute("""
                            SELECT full_name, age, phone_number
                            FROM users
                            WHERE gender = %s AND town = %s AND age BETWEEN %s AND %s
                        """, (opposite_gender, town, min_age, max_age))

                        matches = cursor.fetchall()
                        match_count = len(matches)

                        if match_count > 0:
                            print(f"✅ Found {match_count} matches")

                            # Send total count
                            cursor.execute("""
                                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                                VALUES (%s, %s, %s, 'OUTGOING', NOW())
                            """, (
                                '22141',
                                sender,
                                f"We have {match_count} {'ladies' if opposite_gender == 'Female' else 'gentlemen'} who match your choice! Here are the first 3:"
                            ))

                            connection.commit()

                            # Send the first 3 matches
                            for match in matches[:3]:
                                name, age, phone = match
                                match_msg = f"{name} aged {age}, {phone}"
                                cursor.execute("""
                                    INSERT INTO messages (message_from, message_to, content, direction, date_created)
                                    VALUES (%s, %s, %s, 'OUTGOING', NOW())
                                """, ('22141', sender, match_msg))

                            # Instruction to send NEXT
                            cursor.execute("""
                                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                                VALUES (%s, %s, %s, 'OUTGOING', NOW())
                            """, (
                                '22141',
                                sender,
                                f"Send NEXT to 22141 to receive details of the remaining {match_count - 3} matches."
                                if match_count > 3 else "You have received all available matches."
                            ))

                            connection.commit()
                        else:
                            # No matches
                            cursor.execute("""
                                INSERT INTO messages (message_from, message_to, content, direction, date_created)
                                VALUES (%s, %s, %s, 'OUTGOING', NOW())
                            """, ('22141', sender, "Sorry, no matches were found for your criteria. Try adjusting your age range or town."))
                            connection.commit()
                    else:
                        print("❌ User not found.")
                except ValueError:
                    print("❌ Invalid age range format.")
        else:
            print("❌ Incorrect match format. Should be match#23-25#Nairobi")
    else:
        print("❌ Incorrect message structure. Use match#23-25#Nairobi")
else:
    print("❌ No new 'match#' message found.")

# 5. Close the database connection
cursor.close()
connection.close()