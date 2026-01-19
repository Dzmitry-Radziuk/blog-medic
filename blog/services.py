from typing import Any

from .models import PostView


def add_post_view(post: Any, session_key: str) -> None:
    """Добавляет просмотр поста для заданного session_key, если его ещё нет."""
    PostView.objects.get_or_create(post=post, session_key=session_key)
