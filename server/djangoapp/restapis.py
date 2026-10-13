import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "database" / "data"
DEALERS_FILE = DATA_DIR / "dealerships.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"


def read_data(file_path, key):
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)[key]


def write_reviews(reviews):
    with REVIEWS_FILE.open("w", encoding="utf-8") as file:
        json.dump({"reviews": reviews}, file, indent=2)


def get_request(endpoint, **kwargs):
    endpoint = endpoint.strip("/")

    if endpoint == "fetchDealers":
        return read_data(DEALERS_FILE, "dealerships")

    if endpoint.startswith("fetchDealers/"):
        state = endpoint.split("/", 1)[1]
        return [
            dealer
            for dealer in read_data(DEALERS_FILE, "dealerships")
            if dealer.get("state", "").lower() == state.lower()
        ]

    if endpoint.startswith("fetchDealer/"):
        dealer_id = int(endpoint.rsplit("/", 1)[1])
        dealer = next(
            (
                item
                for item in read_data(DEALERS_FILE, "dealerships")
                if int(item.get("id", 0)) == dealer_id
            ),
            None,
        )
        return dealer

    if endpoint == "fetchReviews":
        return read_data(REVIEWS_FILE, "reviews")

    if endpoint.startswith("fetchReviews/dealer/"):
        dealer_id = int(endpoint.rsplit("/", 1)[1])
        return [
            review
            for review in read_data(REVIEWS_FILE, "reviews")
            if int(review.get("dealership", 0)) == dealer_id
        ]

    raise ValueError(f"Unsupported API endpoint: {endpoint}")


def post_review(data_dict):
    reviews = read_data(REVIEWS_FILE, "reviews")
    next_id = max((int(item.get("id", 0)) for item in reviews), default=0) + 1

    review = {
        "id": next_id,
        "name": data_dict.get("name", ""),
        "dealership": int(data_dict.get("dealership", 0)),
        "review": data_dict.get("review", ""),
        "purchase": data_dict.get("purchase") is True
        or str(data_dict.get("purchase", "")).lower() == "true",
        "purchase_date": data_dict.get("purchase_date", ""),
        "car_make": data_dict.get("car_make", ""),
        "car_model": data_dict.get("car_model", ""),
        "car_year": int(data_dict.get("car_year") or 0),
    }

    reviews.append(review)
    write_reviews(reviews)
    return review


def analyze_review_sentiments(text):
    # A lightweight fallback for deployments without the separate Flask service.
    positive_words = {
        "amazing", "excellent", "fantastic", "good", "great",
        "happy", "love", "positive", "wonderful", "helpful",
    }
    negative_words = {
        "awful", "bad", "horrible", "negative", "poor",
        "terrible", "unhappy", "worst",
    }
    words = set(text.lower().replace(".", " ").replace(",", " ").split())
    positive = len(words & positive_words)
    negative = len(words & negative_words)

    if positive > negative:
        sentiment = "positive"
    elif negative > positive:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {"sentiment": sentiment}
