from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

react_page = TemplateView.as_view(template_name="react_index.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),

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
