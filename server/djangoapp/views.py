import json
import logging
from pathlib import Path

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .restapis import (
    get_request,
    post_review,
    analyze_review_sentiments,
)

logger = logging.getLogger(__name__)


def error_response(message, status=500):
    return JsonResponse({"status": status, "error": message}, status=status)


def read_json(request):
    try:
        return json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return error_response("POST required", 405)

    data = read_json(request)
    if data is None:
        return error_response("Invalid JSON", 400)

    username = data.get("userName", data.get("username", "")).strip()
    password = data.get("password", "")

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"userName": username, "error": "Invalid credentials"})

    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


@csrf_exempt
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return error_response("POST required", 405)

    data = read_json(request)
    if data is None:
        return error_response("Invalid JSON", 400)

    username = data.get("userName", data.get("username", "")).strip()
    first_name = data.get("firstName", data.get("first_name", "")).strip()
    last_name = data.get("lastName", data.get("last_name", "")).strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not all([username, first_name, last_name, email, password]):
        return error_response("All fields are required", 400)

    if User.objects.filter(username=username).exists():
        return error_response("Username already exists", 400)

    if User.objects.filter(email=email).exists():
        return error_response("Email already exists", 400)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )
    return JsonResponse({"userName": user.username, "status": "Registered"}, status=201)


def get_dealerships(request, state=None):
    try:
        if state and state.lower() != "all":
            dealers = get_request(f"fetchDealers/{state}")
        else:
            dealers = get_request("fetchDealers")
        return JsonResponse({"status": 200, "dealers": dealers})
    except Exception:
        logger.exception("Could not fetch dealerships")
        return error_response("Could not fetch dealerships")


def get_dealer_details(request, dealer_id):
    try:
        dealer = get_request(f"fetchDealer/{dealer_id}")
        return JsonResponse({"status": 200, "dealer": [dealer]})
    except Exception:
        logger.exception("Could not fetch dealership details")
        return error_response("Dealership not found", 404)


def get_dealer_reviews(request, dealer_id=None):
    try:
        endpoint = "fetchReviews" if dealer_id is None else f"fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        for review in reviews:
            review_text = str(review.get("review", ""))
            try:
                sentiment_result = analyze_review_sentiments(review_text)
                review["sentiment"] = sentiment_result.get("sentiment", "neutral")
            except Exception:
                logger.warning("Sentiment service unavailable; using neutral fallback")
                review["sentiment"] = "neutral"

        return JsonResponse({"status": 200, "reviews": reviews})
    except Exception:
        logger.exception("Could not fetch reviews")
        return error_response("Could not fetch reviews")


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return error_response("POST required", 405)

    data = read_json(request)
    if data is None:
        return error_response("Invalid JSON", 400)

    required_fields = [
        "name", "dealership", "review", "purchase",
        "purchase_date", "car_make", "car_model", "car_year"
    ]
    if any(field not in data for field in required_fields):
        return error_response("Review data is incomplete", 400)

    try:
        saved_review = post_review(data)
        return JsonResponse({"status": 200, "review": saved_review})
    except Exception:
        logger.exception("Could not submit review")
        return error_response("Could not submit review")


def get_cars(request):
    try:
        inventory_file = (
            Path(settings.BASE_DIR) / "database" / "data" / "car_records.json"
        )
        with inventory_file.open("r", encoding="utf-8") as file:
            inventory = json.load(file)

        unique_cars = {}
        for car in inventory.get("cars", []):
            key = (car.get("make", ""), car.get("model", ""))
            if all(key):
                unique_cars[key] = {
                    "CarMake": key[0],
                    "CarModel": key[1],
                }

        return JsonResponse({
            "status": 200,
            "CarModels": list(unique_cars.values()),
        })
    except Exception:
        logger.exception("Could not load car inventory")
        return error_response("Could not load car inventory")


@csrf_exempt
def analyze_review(request):
    if request.method != "POST":
        return error_response("POST required", 405)

    data = read_json(request)
    if data is None:
        return error_response("Invalid JSON", 400)

    review_text = data.get("review", "")
    if not isinstance(review_text, str) or not review_text.strip():
        return error_response("A review is required", 400)

    try:
        result = analyze_review_sentiments(review_text)
        return JsonResponse({
            "status": 200,
            "review": review_text,
            "sentiment": result.get("sentiment", "neutral"),
        })
    except Exception:
        logger.exception("Could not analyze review sentiment")
        return error_response("Could not analyze review sentiment")
