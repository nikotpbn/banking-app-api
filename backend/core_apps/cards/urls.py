from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import VirtualCardViewSet, VirtualCardTopUpAPIView

router = SimpleRouter()

router.register(r"virtual-cards", VirtualCardViewSet)

urlpatterns = [
    path(
        "virtual-cards/<uuid:pk>/top-up/",
        VirtualCardTopUpAPIView.as_view(),
        name="virtual-card-top-up",
    ),
]

urlpatterns += router.urls