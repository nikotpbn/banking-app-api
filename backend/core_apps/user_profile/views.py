from django.db import transaction
from typing import Any, List
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, generics, viewsets
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.request import Request

from core_apps.common.models import ContentView
from core_apps.common.permissions import IsBranchManager
from core_apps.accounts.utils import create_bank_account
from core_apps.accounts.models import BankAccount
from core_apps.common.renderers import GenericJsonRenderer
from .models import Profile, NextOfKin
from .serializers import NextOfKinSerializer, ProfileListSerializzer, ProfileSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileListSerializzer
    pagination_class = StandardResultsSetPagination
    object_label = "profiles"
    permission_classes = [IsBranchManager]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["user__first_name", "user__last_name", "user__id_no"]
    filterset_fields = ["user__first_name", "user__last_name", "user__id_no"]

    def get_queryset(self) -> List[Profile]:
        return Profile.objects.exclude(user__is_staff=True).exclude(
            user__is_superuser=True
        )


class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    object_label = "profile"

    def get_object(self) -> Profile:
        try:
            profile = Profile.objects.get(user=self.request.user)
            self.record_profile_view(profile)
            return profile

        except:
            raise Http404("Profile not found")


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            updated_instance = serializer.save()
            if updated_instance.is_complete_with_next_of_kin():
                existing_account = BankAccount.objects.filter(
                    user=request.user,
                    currency=updated_instance.account_currency,
                    account_type=updated_instance.account_type,
                ).first()

                if not existing_account:
                    bank_account = create_bank_account(
                        user=request.user,
                        currency=updated_instance.account_currency,
                        account_type=updated_instance.account_type,
                    )

                    message = (
                        "Profile update and bank account created successfully."
                        " An email has been sent to you with further instructions"
                    )
                else:
                    message = "Profile updated successfully."

                return Response(
                    {"message": message, "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "Profile updated successfully. Please complete all required "
                        "fields and at least one next of kin to create a bank account",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

        return Response(serializer.data)

    def record_profile_view(self, profile: Profile) -> None:
        content_type = ContentType.objects.get_for_model(profile)
        viewer_ip = self.get_client_ip()
        user = self.request.user

        object, created = ContentView.objects.update_or_create(
            content_type=content_type,
            object_id=profile.id,
            user=self.request.user,
            viewer_ip=viewer_ip,
            defaults={
                "last_viewed": timezone.now(),
            },
        )

    def get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR", "")
        return ip


class NextOfKinModelViewSet(viewsets.ModelViewSet):
    """
    Most views that were overriden by the tutor
    do exactly the same thing as implemented in the
    Mixins. Thus, only functions there have different
    actions were actually maintained.

    Furthermore, instead of having two different views
    with ListCreateAPIView and RetrieveUpdateDestroyAPIView
    its cleaner and more elegant to have a single ModelViewSet
    which includes all the generics APIViews.
    """

    queryset = NextOfKin.objects.all()
    serializer_class = NextOfKinSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [GenericJsonRenderer]
    object_label = "next_of_kin"

    def get_queryset(self) -> List[NextOfKin]:
        qs = super().get_queryset()
        return qs.filter(profile=self.request.user.profile)

    def get_object(self) -> NextOfKin:
        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self) -> dict[str, Any]:
        ctx = super().get_serializer_context()
        ctx["profile"] = self.request.user.profile
        return ctx

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Next of kin deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
