from django.contrib import admin
from cloudinary.forms import CloudinaryFileField
from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import NextOfKin, Profile


class ProfileAdminForm(forms.ModelForm):
    photo = CloudinaryFileField(
        options={"crop": "thumb", "wdith": 200, "height": 200, "folder": "bank_photo"},
        required=False,
    )

    class Meta:
        model = Profile
        fields = "__all__"


class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 1
    fields = [
        "first_name",
        "last_name",
        "relationship",
        "phone_number",
        "is_primary",
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = [
        "user",
        "full_name",
        "phone_number",
        "email",
        "employment_status",
        "photo_preview",
    ]
    list_display_links = ["user"]
    list_filter = ["gender", "marital_status", "employment_status", "country"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone_number",
    ]
    fieldsets = (
        (
            _("Personal Information"),
            {
                "fields": (
                    "user",
                    "photo",
                    "id_photo",
                    "signature_photo",
                    "gender",
                    "date_of_birth",
                    "marital_status",
                )
            },
        ),
        (
            _("Contat Information"),
            {"fields": ("phone_number", "address", "city", "country")},
        ),
        (
            _("Identification"),
            {
                "fields": (
                    "identification_type",
                    "id_issue_date",
                    "id_expiry_date",
                    "passport_number",
                )
            },
        ),
        (
            _("Employment Information"),
            {
                "fields": (
                    "employment_status",
                    "employer_name",
                    "annual_income",
                    "date_of_employment",
                    "employer_address",
                    "employer_city",
                    "employer_state",
                )
            },
        ),
    )

    inlines = [NextOfKinInline]

    def full_name(self, obj) -> str:
        return obj.user.full_name

    full_name.short_description = _("Full Name")

    def email(self, obj) -> str:
        return obj.user.email

    email.short_description = _("Email")

    def photo_preview(self, obj) -> str:
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover;">',
                obj.photo.url,
            )
        return _("No Photo")

    photo_preview.short_description = _("Photo")

    @admin.register(NextOfKin)
    class NextOfKinAdmin(admin.ModelAdmin):
        list_display = ["full_name", "relationship", "profile", "is_primary"]
        list_filter = ["relationship", "is_primary"]
        search_fields = ["first_name", "last_name", "profile__user__email"]

        def full_name(self, obj) -> str:
            return f"{obj.first_name}  {obj.last_name}"

        full_name.short_description = _("Full Name")
