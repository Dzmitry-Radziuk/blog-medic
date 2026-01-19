import os
import re

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .constants import IMG_SRC_REGEX
from .models import Post


@receiver(post_delete, sender=Post)
def delete_post_images(sender, instance, **kwargs):
    """Удаляет все изображения поста из контента при его удалении."""

    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

    if instance.content:
        matches = re.findall(IMG_SRC_REGEX, instance.content)
        for src in matches:
            if src.startswith(settings.MEDIA_URL):
                file_path = os.path.join(
                    settings.MEDIA_ROOT, src.replace(settings.MEDIA_URL, "")
                )
                if os.path.isfile(file_path):
                    os.remove(file_path)
