# backend/api/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Count, Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

from .models import Message, User, MatchTracking
import json
from datetime import datetime, timedelta
from django.db import transaction

@api_view(['GET'])
@permission_classes([AllowAny])  # Changed from IsAuthenticated
def user_list_view(request):
    """
    Kept as a function-based compatibility stub in case other code references it.
    Primary paginated implementation is the class-based UserListView below.
    """
    return JsonResponse({"detail": "Use the class-based /users/ endpoint (GET) for paginated results."}, status=200)


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
    """
    Paginated, searchable list of users.
    - ?page=<n>    (PageNumberPagination)
    - ?search=<q>  (searches full_name and phone_number)
    Response: DRF-style paginated response with count/next/previous/results.
    """
    permission_classes = [AllowAny]  # Changed from IsAuthenticated

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
    permission_classes = [AllowAny]

    def get(self, request):
        users_by_day = (
            User.objects.extra(select={'day': "DATE(date_created)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        return Response(users_by_day)


class MessageVolumeChart(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        messages_by_day = (
            Message.objects.extra(select={'day': "DATE(date_created)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        return Response(messages_by_day)


class TopCountiesChart(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        counties = (
            User.objects.values("county")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        return Response(counties)


class DescriptionVolumeChart(APIView):
    permission_classes = [AllowAny]

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
# Note: I preserved your original handlers and added missing behaviors below.
# The original logic remains intact; additions are implemented in helper sections.

def handle_sms_command(sender, content):
    content = content.strip()
    lower_content = content.lower()

    # keep compatibility with original detection while adding new formats
    if lower_content.startswith("start#"):
        return handle_start(sender, content)
    elif lower_content.startswith("details#"):
        return handle_details(sender, content)
    elif lower_content.startswith("myself#") or lower_content.startswith("myself"):
        return handle_myself(sender, content)
    elif lower_content.startswith("match#"):
        # new: support match#min-max#town
        return handle_match(sender, content)
    elif lower_content == "next" or lower_content == "next#":
        return handle_next(sender)
    elif lower_content == "yes":
        return handle_yes(sender)
    elif lower_content.startswith("describe#") or lower_content.startswith("describe"):
        return handle_describe(sender, content)
    elif content.startswith("07") and len(content.strip()) >= 10:
        # phone lookup (at least 10 chars, keep original behavior)
        return handle_profile_request(sender, content)
    else:
        # fallback to original check that lowercased content could match
        c = content.strip().lower()
        if c.startswith("start#"):
            return handle_start(sender, content)
        elif c.startswith("details#"):
            return handle_details(sender, content)
        elif c.startswith("myself#"):
            return handle_myself(sender, content)
        elif c == "match#":
            return handle_match(sender)
        elif c == "next#":
            return handle_next(sender)
        elif c == "yes":
            return handle_yes(sender)
        elif c.startswith("describe#"):
            return handle_describe(sender, content)
        elif c.startswith("07") and len(c) == 10:
            return handle_profile_request(sender, content)
        else:
            return "Sorry, invalid command. Send HELP for assistance."


# --- Existing handlers preserved exactly as you provided, then augmented where necessary ---

def handle_start(sender, content):
    try:
        # original logic preserved
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

        # Augmented message to follow project guide (keeps original behavior too)
        msg = f"Your profile has been created successfully {full_name}.\n" \
              "SMS details#levelOfEducation#profession#maritalStatus#religion#ethnicity to 22141.\n" \
              "E.g., details#diploma#driver#single#christian#mijikenda"

        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=msg,
            direction="OUTGOING",
            date_created=timezone.now()
        )
        # return original short string for compatibility plus guide message
        return msg
    except Exception as e:
        return f"Failed to register. Ensure correct format: start#name#age#gender#county#town. Error: {e}"


def handle_details(sender, content):
    try:
        # original logic preserved
        _, education, profession, marital_status, religion, ethnicity = content.split("#")
        updated = User.objects.filter(phone_number=sender).update(
            education_level=education,
            profession=profession,
            marital_status=marital_status,
            religion=religion,
            ethnicity=ethnicity,
        )

        # Augmented behavior: if updated exists, instruct user to send MYSELF; if no profile, instruct to register
        if not updated:
            # no user record found
            msg_not_found = "You were not found in our system. Please register first using start#name#age#gender#county#town"
            Message.objects.create(
                message_from="PENZI",
                message_to=sender,
                content=msg_not_found,
                direction="OUTGOING",
                date_created=timezone.now()
            )
            return msg_not_found

        msg = "This is the last stage of registration.\n" \
              "SMS a brief description of yourself to 22141 starting with the word MYSELF.\n" \
              "E.g., MYSELF chocolate, lovely, sexy etc."

        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=msg,
            direction="OUTGOING",
            date_created=timezone.now()
        )
        return msg
    except Exception as e:
        return f"Failed to update details. Ensure correct format: details#... Error: {e}"


def handle_myself(sender, content):
    try:
        # original behavior preserved (supports "myself#desc" and "MYSELF ..." forms)
        if "#" in content:
            _, description = content.split("#", 1)
        else:
            # allow "MYSELF ..." or "myself ..." without #
            description = content[6:].strip()

        User.objects.filter(phone_number=sender).update(self_description=description)
        # Augmented final registration message
        msg = "You are now registered for dating.\n" \
              "To search for a MPENZI, SMS match#ageRange#town to 22141.\n" \
              "E.g., match#23-25#Kisumu"

        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=msg,
            direction="OUTGOING",
            date_created=timezone.now()
        )
        return msg
    except Exception as e:
        return f"Failed to save description. Format: myself#description. Error: {e}"


# Original handle_match preserved but augmented to support age-range and town format
def handle_match(sender, content=None):
    try:
        # If content provided (new format), parse age range and town
        if content and "#" in content:
            parts = content.split("#")
            # expecting format match#23-25#Town
            if len(parts) >= 3:
                age_part = parts[1]
                town = parts[2].strip()
                try:
                    min_age, max_age = map(int, age_part.split("-"))
                except Exception:
                    # fallback to original behavior if parsing fails
                    min_age, max_age = None, None
            else:
                min_age, max_age, town = None, None, None
        else:
            min_age, max_age, town = None, None, None

        user = User.objects.get(phone_number=sender)
        # If age range and town provided, filter accordingly (new guide behavior)
        if min_age is not None and max_age is not None and town:
            matches_qs = User.objects.filter(
                age__gte=min_age,
                age__lte=max_age,
                town__iexact=town
            ).exclude(phone_number=sender).order_by("id")
        else:
            # fallback to original behavior: all other users
            matches_qs = User.objects.exclude(phone_number=sender).order_by("id")

        # If no matches
        if not matches_qs.exists():
            return "No matches found."

        # store match criteria as a hidden marker message so NEXT can re-run same query
        if min_age is not None and max_age is not None and town:
            criteria_marker = f"MATCH_CRITERIA:{min_age}-{max_age}#{town}"
        else:
            criteria_marker = "MATCH_CRITERIA:ALL"

        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=criteria_marker,
            direction="OUTGOING",
            date_created=timezone.now()
        )

        total_matches = matches_qs.count()
        # Introductory message per guide
        gender_word = "ladies" if getattr(user, "gender", "").lower() == "male" else "gentlemen"
        intro = f"We have {total_matches} {gender_word} who match your choice! We will send you details of 3 of them shortly.\n" \
                "To get more details about a lady, SMS her number e.g., 0722010203 to 22141"

        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=intro,
            direction="OUTGOING",
            date_created=timezone.now()
        )

        # Initialize or reset MatchTracking for this user
        mt, created = MatchTracking.objects.get_or_create(phone_number=sender)
        mt.seen_count = 0
        mt.last_updated = timezone.now()
        mt.save()

        # send first batch of up to 3 matches
        return send_next_matches(sender)

    except User.DoesNotExist:
        return "You must register first. Send start#name#age#gender#county#town"
    except Exception as e:
        return f"Error finding match: {e}"


def handle_next(sender):
    # delegate to send_next_matches which uses MATCH_CRITERIA marker + MatchTracking.seen_count
    return send_next_matches(sender)


def send_next_matches(sender):
    try:
        # find latest MATCH_CRITERIA message sent to this user
        criteria_msg = Message.objects.filter(
            message_to=sender,
            message_from="PENZI",
            content__startswith="MATCH_CRITERIA:"
        ).order_by("-date_created").first()

        if not criteria_msg:
            return "No active match search. Send match#ageRange#town first."

        crit = criteria_msg.content.replace("MATCH_CRITERIA:", "").strip()
        if crit == "ALL":
            min_age = None
            max_age = None
            town = None
        else:
            try:
                age_range, town = crit.split("#")
                min_age, max_age = map(int, age_range.split("-"))
                town = town.strip()
            except Exception:
                min_age = None
                max_age = None
                town = None

        # reconstruct queryset based on criteria
        if min_age is not None and max_age is not None and town:
            matches_qs = User.objects.filter(
                age__gte=min_age,
                age__lte=max_age,
                town__iexact=town
            ).exclude(phone_number=sender).order_by("id")
        else:
            matches_qs = User.objects.exclude(phone_number=sender).order_by("id")

        # get or create MatchTracking
        mt, _ = MatchTracking.objects.get_or_create(phone_number=sender)
        start = getattr(mt, "seen_count", 0)
        batch = list(matches_qs[start:start+3])

        if not batch:
            return "No more matches."

        # build message lines for this batch
        msg_lines = []
        for u in batch:
            msg_lines.append(f"{u.full_name} aged {u.age}, {u.phone_number}.")

        remaining = matches_qs.count() - (start + len(batch))
        msg = "\n".join(msg_lines)
        if remaining > 0:
            msg += f"\n\nSend NEXT to 22141 to receive details of the remaining {remaining} { 'ladies' if remaining==1 else 'ladies' }"

        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=msg,
            direction="OUTGOING",
            date_created=timezone.now()
        )

        # update tracking
        mt.seen_count = start + len(batch)
        mt.last_updated = timezone.now()
        mt.save()

        return msg
    except Exception as e:
        return f"Error sending next matches: {e}"


def handle_describe(sender, content):
    try:
        # allow "describe#0722..." or "DESCRIBE 0722..."
        if "#" in content:
            _, target_phone = content.split("#", 1)
            target_phone = target_phone.strip()
        else:
            # split words, pick the first token after 'describe'
            parts = content.strip().split()
            if len(parts) >= 2:
                target_phone = parts[1].strip()
            else:
                return "Invalid format. Use: DESCRIBE <phone>"

        target = User.objects.get(phone_number=target_phone)
        # send the self-description to the requester (as guide indicates)
        msg_to_requester = f"{target.full_name} describes themselves as {target.self_description}"
        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=msg_to_requester,
            direction="OUTGOING",
            date_created=timezone.now()
        )
        # create the interest marker message from requester -> target (so YES can find it)
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
        # find the most recent describe_interest that targets this sender (someone previously requested this person's details)
        last_interest = Message.objects.filter(
            message_to=sender,
            content="describe_interest"
        ).order_by("-date_created").first()

        if not last_interest:
            return "No previous profile viewed. Use describe#..."

        requester_phone = last_interest.message_from
        # fetch both users
        requester = User.objects.get(phone_number=requester_phone)
        responder = User.objects.get(phone_number=sender)

        # notify requester that responder is interested
        Message.objects.create(
            message_from="PENZI",
            message_to=requester_phone,
            content=f"Good news! {responder.full_name} ({responder.phone_number}) is interested in you.",
            direction="OUTGOING",
            date_created=timezone.now()
        )

        # send full requester profile to responder (per guide: show requester details to the responder when responder sends YES)
        full_profile = f"{requester.full_name} aged {requester.age}, {requester.county} County, {requester.town} town, " \
                       f"{requester.education_level}, {requester.profession}, {requester.marital_status}, {requester.religion}, {requester.ethnicity}. " \
                       f"Send DESCRIBE {requester.phone_number} to get more details about {requester.full_name}."

        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=full_profile,
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

        # Send full details + prompt to describe back to requester
        msg_requester = f"{user.full_name}, {user.age}, {user.gender}, {user.county}, {user.town}, {user.profession}, {user.religion}. Description: {user.self_description}. " \
                        f"Send DESCRIBE {user.phone_number} to get more details."

        Message.objects.create(
            message_from="PENZI",
            message_to=sender,
            content=msg_requester,
            direction="OUTGOING",
            date_created=timezone.now()
        )

        # Inform the requested person with requester's basic info
        try:
            requester = User.objects.get(phone_number=sender)
            requester_info = f"{requester.full_name} aged {requester.age} based in {requester.county}"
        except User.DoesNotExist:
            requester_info = "Someone"

        msg_target = f"Hi {user.full_name}, a person called {requester_info} is interested in you and requested your details. Do you want to know more about them? Send YES to 22141"

        Message.objects.create(
            message_from="PENZI",
            message_to=number,
            content=msg_target,
            direction="OUTGOING",
            date_created=timezone.now()
        )

        return "Profile sent."
    except User.DoesNotExist:
        return "User not found."
    except Exception as e:
        return f"Error sending profile: {e}"
