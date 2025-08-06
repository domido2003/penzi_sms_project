from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

from .models import Message, User, MatchTracking

import json
from datetime import datetime
from datetime import datetime
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    ...

@csrf_exempt
@require_http_methods(["GET", "POST"])
def message_list_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("📥 Received data:", data)

            message = Message.objects.create(
                message_from=data["message_from"],
                message_to="PENZI",
                content=data["content"],
                direction="INCOMING",
                date_created=timezone.now()
            )

            response = handle_sms_command(data["message_from"], data["content"])
            return JsonResponse({"message": response}, status=201)

        except Exception as e:
            print("❌ Error:", e)
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":
        messages = list(
            Message.objects.all()
            .order_by("-date_created")
            .values("id", "message_from", "message_to", "content", "direction", "date_created")
        )
        return JsonResponse(messages, safe=False)

class SMSHandlerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            sender = data.get("message_from")
            content = data.get("content")

            Message.objects.create(
                message_from=sender,
                message_to="PENZI",
                content=content,
                direction="INCOMING",
                date_created=timezone.now()
            )

            response = handle_sms_command(sender, content)

            return Response({"message": response}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 30

        query = request.GET.get("search", "").strip()

        user_queryset = User.objects.all().order_by("-date_created")

        if query:
            user_queryset = user_queryset.filter(
                Q(full_name__icontains=query) |
                Q(phone_number__icontains=query)
            )

        user_queryset = user_queryset.values(
            "id", "full_name", "phone_number", "age", "gender", "county", "town",
            "education_level", "profession", "marital_status", "religion",
            "ethnicity", "self_description", "date_created"
        )

        result_page = paginator.paginate_queryset(user_queryset, request)
        return paginator.get_paginated_response(result_page)


class UserGrowthChart(APIView):
    def get(self, request):
        users_by_day = (
            User.objects.extra(select={'day': "DATE(date_created)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        return Response(users_by_day)

class MessageVolumeChart(APIView):
    def get(self, request):
        messages_by_day = (
            Message.objects.extra(select={'day': "DATE(date_created)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        return Response(messages_by_day)

class TopCountiesChart(APIView):
    def get(self, request):
        counties = (
            User.objects.values("county")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        return Response(counties)

class DescriptionVolumeChart(APIView):
    def get(self, request):
        desc_stats = (
            User.objects.exclude(self_description__isnull=True)
            .exclude(self_description__exact="")
            .extra(select={'day': "DATE(date_created)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        return Response(desc_stats)

# ---------------------------- SMS Command Handlers ----------------------------

def handle_sms_command(sender, content):
    content = content.strip().lower()

    if content.startswith("start#"):
        return handle_start(sender, content)
    elif content.startswith("details#"):
        return handle_details(sender, content)
    elif content.startswith("myself#"):
        return handle_myself(sender, content)
    elif content == "match#":
        return handle_match(sender)
    elif content == "next#":
        return handle_next(sender)
    elif content == "yes":
        return handle_yes(sender)
    elif content.startswith("describe#"):
        return handle_describe(sender, content)
    elif content.startswith("07") and len(content) == 10:
        return handle_profile_request(sender, content)
    else:
        return "Sorry, invalid command. Send HELP for assistance."

def handle_start(sender, content):
    try:
        _, full_name, age, gender, county, town = content.split("#")
        User.objects.update_or_create(
            phone_number=sender,
            defaults={
                "full_name": full_name,
                "age": int(age),
                "gender": gender,
                "county": county,
                "town": town,
                "date_created": timezone.now()
            },
        )
        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content="Your profile has been created. Now send: details#education#profession#marital status#religion#ethnicity",
            direction="OUTGOING",
            date_created=timezone.now()
        )
        return "Your profile has been created. Now send: details#education#profession#marital status#religion#ethnicity"
    except Exception as e:
        return f"Failed to register. Ensure correct format: start#name#age#gender#county#town. Error: {e}"

def handle_details(sender, content):
    try:
        _, education, profession, marital_status, religion, ethnicity = content.split("#")
        User.objects.filter(phone_number=sender).update(
            education_level=education,
            profession=profession,
            marital_status=marital_status,
            religion=religion,
            ethnicity=ethnicity,
        )
        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content="Profile updated. To describe yourself, send: myself#description",
            direction="OUTGOING",
            date_created=timezone.now()
        )
        return "Profile updated. To describe yourself, send: myself#description"
    except Exception as e:
        return f"Failed to update details. Ensure correct format: details#... Error: {e}"

def handle_myself(sender, content):
    try:
        _, description = content.split("#", 1)
        User.objects.filter(phone_number=sender).update(self_description=description)
        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content="Description saved. To request a match, send: match#",
            direction="OUTGOING",
            date_created=timezone.now()
        )
        return "Description saved. To request a match, send: match#"
    except Exception as e:
        return f"Failed to save description. Format: myself#description. Error: {e}"

def handle_match(sender):
    try:
        user = User.objects.get(phone_number=sender)
        matches = User.objects.exclude(phone_number=sender).order_by("id")
        for match in matches:
            if not Message.objects.filter(
                message_from=sender,
                message_to=match.phone_number,
                content__icontains="describe"
            ).exists():
                Message.objects.create(
                    message_from="PENZI",
                    message_to=sender,
                    content=f"Potential match: {match.full_name}, {match.age}, {match.county}. To know more, send: describe#{match.phone_number}",
                    direction="OUTGOING",
                    date_created=timezone.now()
                )
                return f"Potential match sent: {match.phone_number}"
        return "No matches found."
    except Exception as e:
        return f"Error finding match: {e}"

def handle_next(sender):
    return handle_match(sender)

def handle_describe(sender, content):
    try:
        _, target_phone = content.split("#")
        target = User.objects.get(phone_number=target_phone)
        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=f"{target.full_name}, {target.age}, {target.gender}, {target.county}, {target.town}, {target.profession}, {target.religion}. Description: {target.self_description}\nInterested? Send YES.",
            direction="OUTGOING",
            date_created=timezone.now()
        )
        Message.objects.create(
            message_from=sender,
            message_to=target_phone,
            content="describe_interest",
            direction="OUTGOING",
            date_created=timezone.now()
        )
        return "Profile sent. Send YES if interested."
    except User.DoesNotExist:
        return "User not found."
    except Exception as e:
        return f"Failed to describe: {e}"

def handle_yes(sender):
    try:
        last_interest = Message.objects.filter(
            message_from=sender, content="describe_interest"
        ).order_by("-date_created").first()

        if not last_interest:
            return "No previous profile viewed. Use describe#..."

        target_phone = last_interest.message_to
        requester = User.objects.get(phone_number=target_phone)
        responder = User.objects.get(phone_number=sender)

        Message.objects.create(
            message_from="PENZI",
            message_to=target_phone,
            content=f"Good news! {responder.full_name} ({responder.phone_number}) is interested in you.",
            direction="OUTGOING",
            date_created=timezone.now()
        )

        return f"You showed interest in {requester.full_name}. They've been notified."
    except Exception as e:
        return f"Error confirming interest: {e}"

def handle_profile_request(sender, content):
    try:
        number = content.strip()
        user = User.objects.get(phone_number=number)
        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=f"{user.full_name}, {user.age}, {user.gender}, {user.county}, {user.town}, {user.profession}, {user.religion}. Description: {user.self_description}",
            direction="OUTGOING",
            date_created=timezone.now()
        )
        Message.objects.create(
            message_from="PENZI",
            message_to=number,
            content=f"Someone is interested in you on PENZI. Stay tuned!",
            direction="OUTGOING",
            date_created=timezone.now()
        )
        return "Profile sent."
    except User.DoesNotExist:
        return "User not found."
