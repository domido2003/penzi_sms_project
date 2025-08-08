from mailbox import Message
from django.http import JsonResponse
import mysql.connector

try:
    # 1. Connect to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="domido2003",
        database="penzi_dating"
    )
    cursor = connection.cursor()

    # 2. Fetch the latest 'start#' message
    cursor.execute("""
        SELECT id, message_from, content FROM messages
        WHERE direction = 'INCOMING' AND content LIKE 'start#%'
        ORDER BY date_created DESC
        LIMIT 1
    """)
    message = cursor.fetchone()

    if message:
        msg_id, sender, content = message
        print(f"Received message: {content}")

        # 3. Split and validate the message format
        parts = content.strip().split("#")
        if len(parts) == 6:
            _, full_name, age, gender, county, town = parts

            try:
                # 4. Insert the new user into the users table
                cursor.execute("""
                    INSERT INTO users (full_name, phone_number, age, gender, county, town)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (full_name, sender, int(age), gender, county, town))
                connection.commit()
                print(f" User {full_name} registered successfully.")

                # 5. Send welcome message + instruction for next step
                welcome_message = (
                    "Welcome to our dating service with 6000 potential dating partners! "
                    "To complete your profile, SMS details#levelOfEducation#profession#maritalStatus#religion#ethnicity to 22141.\n"
                    "E.g. details#diploma#driver#single#christian#mijikenda"
                )
                cursor.execute("""
                    INSERT INTO messages (message_from, message_to, content, direction, date_created)
                    VALUES (%s, %s, %s, 'OUTGOING', NOW())
                """, ('22141', sender, welcome_message))
                connection.commit()

            except mysql.connector.Error as err:
                print(" Error while inserting user:", err)
        else:
            print("Incorrect format. Use: start#Name#Age#Gender#County#Town")
    else:
        print(" No new 'start#' message found.")

except Exception as e:
    print(" General error:", str(e))

finally:
    try:
        cursor.close()
        connection.close()
    except:
        pass


from django.views.decorators.http import require_GET

@require_GET
def message_list(request):
    messages = Message.objects.all().order_by('-date_created')
    data = [
        {
            "message_from": msg.message_from,
            "message_to": msg.message_to,
            "content": msg.content,
            "direction": msg.direction,
            "date_created": msg.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for msg in messages
    ]
    return JsonResponse(data, safe=False)
