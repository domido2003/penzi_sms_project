from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Message, User
from django.db.models import Q
from datetime import datetime
import json
import re

@csrf_exempt
@require_http_methods(["POST"])
def sms_handler(request):
    try:
        data = json.loads(request.body)
        sender = data.get("message_from")
        recipient = data.get("message_to", "22141")
        content = data.get("content", "").strip()
        direction = data.get("direction", "INCOMING")

        if not sender or not content:
            return JsonResponse({"error": "Missing sender or content."}, status=400)

        # Save incoming message
        Message.objects.create(
            message_from=sender,
            message_to=recipient,
            content=content,
            direction=direction,
            date_created=datetime.now()
        )

        response_messages = []

        # START#...
        if content.lower().startswith("start#"):
            parts = content.split("#")
            if len(parts) == 6:
                _, full_name, age, gender, county, town = parts
                User.objects.create(
                    full_name=full_name.strip(),
                    phone_number=sender,
                    age=int(age.strip()),
                    gender=gender.strip(),
                    county=county.strip(),
                    town=town.strip()
                )
                response_messages.append(
                    "Welcome to our dating service with 6000 potential dating partners! "
                    "To complete your profile, SMS details#levelOfEducation#profession#maritalStatus#religion#ethnicity to 22141.\n"
                    "E.g. details#diploma#driver#single#christian#mijikenda"
                )
            else:
                response_messages.append("Incorrect format. Use: start#Name#Age#Gender#County#Town")

        # DETAILS#...
        elif content.lower().startswith("details#"):
            parts = content.split("#")
            if len(parts) == 6:
                _, edu, job, status, religion, tribe = parts
                updated = User.objects.filter(phone_number=sender).update(
                    education_level=edu.strip(),
                    profession=job.strip(),
                    marital_status=status.strip(),
                    religion=religion.strip(),
                    ethnicity=tribe.strip()
                )
                if updated:
                    response_messages.append("Your profile has been updated successfully. This is the last stage of registration. "
                                             "SMS a brief description of yourself to 22141 starting with the word MYSELF.")
                else:
                    response_messages.append("No matching user found. Please register first using start#...")
            else:
                response_messages.append("Incorrect format. Use: details#edu#job#marital#religion#tribe")

        # MYSELF ...
        elif content.upper().startswith("MYSELF"):
            description = content[6:].strip()
            if description:
                updated = User.objects.filter(phone_number=sender).update(self_description=description)
                if updated:
                    response_messages.append("Your profile has been updated successfully. You are now fully registered for dating. "
                                             "To find a MPENZI, SMS match#ageRange#town to 22141. For example, match#25-30#Nairobi")
                else:
                    response_messages.append("We could not find your account to update the profile. Please register first using start#...")
            else:
                response_messages.append("Please include a description after the word MYSELF. Example: MYSELF kind, honest, and caring.")

        # MATCH#...
        elif content.lower().startswith("match#"):
            try:
                _, rest = content.split("#", 1)
                age_range, town = rest.split("#")
                min_age, max_age = map(int, age_range.split("-"))

                sender_gender = User.objects.get(phone_number=sender).gender.lower()
                opposite_gender = "female" if sender_gender == "male" else "male"

                matches = User.objects.filter(
                    gender__iexact=opposite_gender,
                    town__iexact=town.strip(),
                    age__gte=min_age,
                    age__lte=max_age
                ).exclude(phone_number=sender)

                count = matches.count()
                if count > 0:
                    response_messages.append(
                        f"We have {count} {'ladies' if opposite_gender == 'female' else 'gentlemen'} who match your choice! Here are the first 3:")
                    for match in matches[:3]:
                        response_messages.append(f"{match.full_name} aged {match.age}, {match.phone_number}")
                    if count > 3:
                        response_messages.append(f"Send NEXT to 22141 to receive details of the remaining {count - 3} matches.")
                    else:
                        response_messages.append("You have received all available matches.")
                else:
                    response_messages.append("Sorry, no matches were found for your criteria. Try adjusting your age range or town.")
            except:
                response_messages.append("Incorrect match format. Use match#23-25#Nairobi")

        # NEXT
        elif content.upper() == "NEXT":
            try:
                sender_gender = User.objects.get(phone_number=sender).gender.lower()
                opposite_gender = "female" if sender_gender == "male" else "male"
                from .models import MatchTracking
                track = MatchTracking.objects.filter(phone_number=sender).first()
                offset = track.seen_count if track else 3

                matches = User.objects.filter(
                    gender__iexact=opposite_gender
                ).exclude(phone_number=sender)[offset:offset+3]

                if matches:
                    if track:
                        track.seen_count += 3
                        track.save()
                    else:
                        MatchTracking.objects.create(phone_number=sender, seen_count=6)

                    for match in matches:
                        response_messages.append(f"{match.full_name} aged {match.age}, {match.phone_number}.")
                    response_messages.append("Send the number of someone you're interested in to get their full profile. "
                                             "E.g., 0702556677. To see more matches, reply with NEXT.")
                else:
                    response_messages.append("No more matches available at the moment.")
            except:
                response_messages.append("Unable to complete YES request. No recent interest message found. Please make sure someone requested your profile first.")


        # DESCRIBE 07...
        elif content.upper().startswith("DESCRIBE"):
            parts = content.strip().split()
            if len(parts) == 2:
                target = parts[1].strip()
                try:
                    match = User.objects.get(phone_number=target)
                    response_messages.append(f"{match.full_name} describes themselves as: {match.self_description}")

                    req = User.objects.get(phone_number=sender)
                    notification = f"Hi {match.full_name}, a person called {req.full_name} is interested in you and requested your details. " \
                                   f"He is aged {req.age} and based in {req.county}, {req.town}. Do you want to know more about him? Reply with YES to 22141."
                    Message.objects.create(message_from="22141", message_to=target, content=notification,
                                           direction="OUTGOING", date_created=datetime.now())
                except:
                    response_messages.append("Target user not found.")
            else:
                response_messages.append("Invalid DESCRIBE format. Use: DESCRIBE 07XXXXXXXX")

        # YES
        elif content.upper() == "YES":
            try:
                msg = Message.objects.filter(
                    direction="OUTGOING",
                    content__icontains="requested your details",
                    message_to=sender
                ).order_by("-date_created").first()

                if msg:
                    requester = msg.message_from
                    interested_user = User.objects.get(phone_number=requester)

                    profile_message = (
                        f"{interested_user.full_name}, aged {interested_user.age}, {interested_user.county} County, "
                        f"{interested_user.town} town, {interested_user.education_level}, {interested_user.profession}, "
                        f"{interested_user.marital_status}, {interested_user.religion}, {interested_user.ethnicity}."
                    )
                    if interested_user.self_description:
                        profile_message += f" Self-description: {interested_user.self_description}"

                    Message.objects.create(
                        message_from="22141",
                        message_to=sender,
                        content=profile_message,
                        direction="OUTGOING",
                        date_created=datetime.now()
                    )
                else:
                    Message.objects.create(
                        message_from="22141",
                        message_to=sender,
                        content="Unable to complete YES request. No interest request found.",
                        direction="OUTGOING",
                        date_created=datetime.now()
                    )
            except Exception as e:
                Message.objects.create(
                    message_from="22141",
                    message_to=sender,
                    content="Unable to complete YES request.",
                    direction="OUTGOING",
                    date_created=datetime.now()
                )

        # 07XXXXXXXX
        elif re.match(r"^07\d{8}$", content):
            try:
                target = User.objects.get(phone_number=content)
                response_messages.append(
                    f"{target.full_name} aged {target.age}, {target.county} County, {target.town} town, {target.education_level}, "
                    f"{target.profession}, {target.marital_status}, {target.religion}, {target.ethnicity}. "
                    f"Send DESCRIBE {target.phone_number} to get more details about {target.full_name}."
                )
                req = User.objects.get(phone_number=sender)
                notify = f"Hi {target.full_name}, a user named {req.full_name} is interested in you and requested your details. " \
                         f"They are aged {req.age} based in {req.county}. Do you want to know more about them? Send YES to 22141."
                Message.objects.create(message_from="22141", message_to=target.phone_number, content=notify,
                                       direction="OUTGOING", date_created=datetime.now())
            except:
                response_messages.append("No user found with that number.")

        # Send all response messages
        for msg in response_messages:
            Message.objects.create(
                message_from="22141",
                message_to=sender,
                content=msg,
                direction="OUTGOING",
                date_created=datetime.now()
            )

        return JsonResponse({"responses": response_messages}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def message_list_create(request):
    messages = Message.objects.all().order_by("-date_created")
    data = [
        {
            "message_from": m.message_from,
            "message_to": m.message_to,
            "content": m.content,
            "direction": m.direction,
            "date_created": m.date_created.isoformat(),
        }
        for m in messages
    ]
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def list_users(request):
    users = User.objects.all().values()
    return JsonResponse(list(users), safe=False)
