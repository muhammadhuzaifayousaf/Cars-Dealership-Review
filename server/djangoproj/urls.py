from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from djangoapp.restapis import get_request, analyze_review_sentiments

react_page = TemplateView.as_view(template_name="react_index.html")


@require_GET
def fetch_dealers(request, state=None):
    endpoint = "fetchDealers" if not state else f"fetchDealers/{state}"
    return JsonResponse(get_request(endpoint), safe=False)


@require_GET
def fetch_dealer(request, dealer_id):
    dealer = get_request(f"fetchDealer/{dealer_id}")
    if dealer is None:
        return JsonResponse({"error": "Dealer not found"}, status=404)
    return JsonResponse(dealer)


@require_GET
def fetch_reviews(request, dealer_id):
    return JsonResponse(get_request(f"fetchReviews/dealer/{dealer_id}"), safe=False)


@require_GET
def analyze_review_get(request, review):
    return JsonResponse(analyze_review_sentiments(review))

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),

    path("fetchDealers", fetch_dealers, name="fetch_dealers"),
    path("fetchDealers/<str:state>", fetch_dealers, name="fetch_dealers_by_state"),
    path("fetchDealer/<int:dealer_id>", fetch_dealer, name="fetch_dealer"),
    path("fetchReviews/dealer/<int:dealer_id>", fetch_reviews, name="fetch_reviews_by_dealer"),
    path("analyze/<path:review>", analyze_review_get, name="analyze_review_get"),

    path("about", TemplateView.as_view(template_name="About.html")),
    path("about/", TemplateView.as_view(template_name="About.html")),
    path("contact", TemplateView.as_view(template_name="Contact.html")),
    path("contact/", TemplateView.as_view(template_name="Contact.html")),

    path("", react_page),
    path("login", react_page),
    path("register", react_page),
    path("dealers", react_page),
    path("dealer/<int:dealer_id>", react_page),
    path("postreview/<int:dealer_id>", react_page),

    re_path(
        r"^(?!admin/|djangoapp/|static/|media/|about/?$|contact/?$).*$",
        react_page,
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
