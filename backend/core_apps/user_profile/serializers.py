import base64
from typing import Any, Dict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from core_apps.common.models import ContentView
from .models import Profile, NextOfKin
from .tasks import upload_photos_to_cloudinary

User = get_user_model()


class NextOfKinSerializer(serializers.ModelSerializer):
    """
    The custom uuid field was removed because it is not needed.
    DRF uuid field already converts uuid to string.
    """

    country = CountryField(name_only=True)
    phone_number = PhoneNumberField()

    class Meta:
        model = NextOfKin
        exclude = ["profile"]
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data: Dict) -> NextOfKin:
        profile = self.context.get("profile", None)
        if not profile:
            raise serializers.ValidationError("Profile context is required")

        return NextOfKin.objects.create(profile=profile, **validated_data)


class ProfileSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    date_joined = serializers.DateTimeField(source="user.date_joined")
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "middle_name": {"required": False, "allow_blank": True},
        }

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        id_issue_date = attrs.get("id_issue_date", None)
        id_expiry_date = attrs.get("id_expiry_date", None)

        if id_issue_date and id_expiry_date and id_expiry_date <= id_issue_date:
            raise serializers.ValidationError(
                "ID expiry date must be after the issue date."
            )

        return attrs

    def to_representation(self, instance: Profile) -> dict:
        representation = super().to_representation(instance)

        representation["next_of_kin"] = NextOfKinSerializer(
            instance.next_of_kin.all(), many=True
        ).data

        return representation

    def update(self, instance: Profile, validated_data: dict) -> Profile:
        user_data = validated_data.pop("user", None)

        if user_data:
            for attr, value in user_data.items():
                if attr in ["email", "username"]:
                    setattr(instance.user, attr, value)
            instance.user.save()

        photos_to_upload = {}

        for field in ["photo", "id_photo", "signature_photo"]:
            if field in validated_data:
                photo = validated_data.pop(field, None)
                if photo and photo.size > settings.MAX_UPLOAD_SIZE:
                    temp_file = default_storage.save(
                        f"temp_{instance.id}_{field}.jpg", ContentFile(photo.read())
                    )
                    temp_file_path = default_storage.path(temp_file)
                    photos_to_upload[field] = {
                        "type": "file",
                        "path": temp_file_path,
                        "data": photo,
                    }
                else:
                    image_content = photo.read()
                    encoded_image = base64.b64encode(image_content).decode("utf-8")
                    photos_to_upload[field] = {
                        "type": "base64",
                        "data": encoded_image,
                    }

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if photos_to_upload:
            upload_photos_to_cloudinary.delay(str(instance.id), photos_to_upload)

        return instance

    def get_view_count(self, obj: Profile) -> int:
        """
        Returns the view count for the profile.
        """
        content_type = ContentType.objects.get_for_model(obj)
        return ContentView.objects.filter(
            content_type=content_type, object_id=obj.id
        ).count()


class ProfileListSerializzer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source="user.fullname")
    username = serializers.ReadOnlyField(source="user.username")
    email = serializers.EmailField(source="user.email", read_only=True)
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "full_name",
            "username",
            "gender",
            "nationality",
            "country_of_birth",
            "email",
            "phone_number",
            "photo",
        )

    def get_photo(self, obj: Profile) -> str | None:
        try:
            return obj.photo_url
        except AttributeError:
            return None
