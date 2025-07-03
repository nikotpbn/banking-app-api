from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import NextOfKinModelViewSet, ProfileListAPIView, ProfileDetailAPIView

router = SimpleRouter()

router.register(r"my-profile/next-of-kin", NextOfKinModelViewSet)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all_profiles"),
    path("my-profile/", ProfileDetailAPIView.as_view(), name="my_profile"),
]

urlpatterns += router.urls