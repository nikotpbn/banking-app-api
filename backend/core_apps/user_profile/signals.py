from typing import Any, Type
from django.db.models.base import Model

from django.db.models.signals import post_save
from django.dispatch import receiver
from loguru import logger
from django.contrib.auth import get_user_model
from core_apps.user_profile.models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(
    sender: Type[Model], instance: Model, created: bool, **kwargs: Any
) -> None:
    if created:
        Profile.objects.create(user=instance)
        logger.info(
            f"Profile created for user {instance.first_name} {instance.last_name}"
        )


@receiver(post_save, sender=User)
def save_user_profile(sender: Type[Model], instance: Model, **kwargs: Any) -> None:
    instance.profile.save()
