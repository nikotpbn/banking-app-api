from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]


drf_spectacular = [
    # YOUR PATTERNS
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("core_apps.user_auth.urls")),
    path("api/v1/profiles/", include("core_apps.user_profile.urls")),
    path("api/v1/accounts/", include("core_apps.accounts.urls")),
    path("api/v1/cards/", include("core_apps.cards.urls")),
]
urlpatterns += drf_spectacular

admin.site.site_header = "NextGen Bank Admin"
admin.site.site_title = "NextGen Bank Admin Portal"
admin.site.index_title = "Welcome to NextGen Bank Admin Portal"
