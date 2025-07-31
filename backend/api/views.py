from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET
from .models import Message, User
from datetime import datetime
from math import ceil
import json

from django.db.models.functions import Trunc
from django.db.models import Count


# ✅ Fetch and create messages (GET for listing, POST for simulating)
@csrf_exempt
@require_http_methods(["GET", "POST"])
def message_list_create(request):
    if request.method == "GET":
        messages = Message.objects.all().order_by("-date_created")
        data = [
            {
                "id": m.id,
                "message_from": m.message_from,
                "message_to": m.message_to,
                "content": m.content,
                "direction": m.direction,
                "date_created": m.date_created,
            }
            for m in messages
        ]
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            message_from = data.get("message_from")
            content = data.get("content")

            Message.objects.create(
                message_from=message_from,
                message_to="System",
                content=content,
                direction="INCOMING",
                date_created=datetime.now()
            )

            return JsonResponse({"message": "Message received."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


# ✅ Handles incoming SMS commands like start#, details#, etc.
@csrf_exempt
@require_http_methods(["POST"])
def sms_handler(request):
    try:
        data = json.loads(request.body)
        message_from = data.get("message_from")
        content = data.get("content").strip()
        now = datetime.now()

        # Save the incoming SMS
        Message.objects.create(
            message_from=message_from,
            message_to="System",
            content=content,
            direction="INCOMING",
            date_created=now
        )

        tokens = content.lower().split("#")
        keyword = tokens[0]

        if keyword == "start" and len(tokens) == 6:
            full_name, age, gender, county, town = tokens[1:]
            User.objects.update_or_create(
                phone_number=message_from,
                defaults={
                    "full_name": full_name.title(),
                    "age": int(age),
                    "gender": gender.title(),
                    "county": county.title(),
                    "town": town.title(),
                    "date_created": now,
                }
            )
            response = (
                "✅ Your profile has been created.\n"
                "📌 To complete registration, send:\n"
                "details#education#profession#marital_status#religion#ethnicity"
            )

        elif keyword == "details" and len(tokens) == 6:
            education, profession, marital, religion, ethnicity = tokens[1:]
            User.objects.filter(phone_number=message_from).update(
                education_level=education.title(),
                profession=profession.title(),
                marital_status=marital.title(),
                religion=religion.title(),
                ethnicity=ethnicity.title()
            )
            response = (
                "✅ Your profile has been updated.\n"
                "🎉 You are now fully registered for dating.\n"
                "📌 To find a MPENZI, SMS match#ageRange#town to 22141.\n"
                "📍 Example: match#25-30#Nairobi"
            )

        elif keyword == "myself" and len(tokens) >= 2:
            description = "#".join(tokens[1:])
            User.objects.filter(phone_number=message_from).update(
                self_description=description
            )
            response = (
                "📝 Your self-description has been saved.\n"
                "To start matching, send: match#25-30#Nairobi"
            )

        elif keyword == "match" and len(tokens) == 3:
            response = "🔍 Searching for matches... (feature to be completed)"

        elif keyword == "describe" and len(tokens) == 2:
            phone = tokens[1]
            response = f"📨 Description request for {phone} has been received."

        elif keyword == "yes":
            response = "✅ You accepted the interest. Full profile will be sent soon."

        elif content.strip().startswith("07") and len(content.strip()) == 10:
            response = (
                "📍 You requested someone's profile.\n"
                "They will be notified and must accept before you get their full details."
            )

        else:
            response = (
                "❌ Invalid command format.\n"
                "Start by sending:\n"
                "start#Jane Doe#25#Female#Nairobi#Westlands"
            )

        # Save system response
        Message.objects.create(
            message_from="System",
            message_to=message_from,
            content=response,
            direction="OUTGOING",
            date_created=now
        )

        return JsonResponse({"response": response})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ✅ Paginated user list
@require_http_methods(["GET"])
def user_list(request):
    try:
        page = int(request.GET.get("page", 1))
        per_page = 30
        offset = (page - 1) * per_page

        users_qs = User.objects.all().order_by("-date_created")
        total_users = users_qs.count()
        total_pages = ceil(total_users / per_page)

        users = list(users_qs[offset:offset + per_page].values())

        return JsonResponse({
            "users": users,
            "total_users": total_users,
            "total_pages": total_pages,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ✅ Chart: User growth per day
@require_GET
def user_growth(request):
    data = (
        User.objects
        .filter(date_created__isnull=False)
        .annotate(day=Trunc('date_created', 'day'))
        .values('day')
        .annotate(users=Count('id'))
        .order_by('day')
    )
    formatted = [{"date": d["day"], "users": d["users"]} for d in data]
    return JsonResponse(formatted, safe=False)


# ✅ Chart: Message volume per day
@require_GET
def message_volume(request):
    data = (
        Message.objects
        .filter(date_created__isnull=False)
        .annotate(day=Trunc('date_created', 'day'))
        .values('day')
        .annotate(messages=Count('id'))
        .order_by('day')
    )
    formatted = [{"date": d["day"], "messages": d["messages"]} for d in data]
    return JsonResponse(formatted, safe=False)


# ✅ Chart: Top counties by number of users
@require_GET
def top_counties(request):
    data = (
        User.objects
        .exclude(county__isnull=True)
        .exclude(county__exact='')
        .values("county")
        .annotate(users=Count("id"))
        .order_by("-users")[:10]
    )
    return JsonResponse(list(data), safe=False)


# ✅ Chart: Self-description volume (who described themselves)
@require_GET
def description_volume(request):
    described = User.objects.filter(self_description__isnull=False).exclude(self_description="").count()
    not_described = User.objects.filter(self_description__isnull=True) | User.objects.filter(self_description="")
    not_described_count = not_described.count()

    data = [
        {"label": "Described", "count": described},
        {"label": "Not Described", "count": not_described_count},
    ]
    return JsonResponse(data, safe=False)
