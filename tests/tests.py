"""Тесты приложения blog."""

import pytest
from http import HTTPStatus
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.urls import reverse

from blog.models import Post, PostView
from blog.services import add_post_view
from blog.validators import validate_title
from tests.constants import (
    TEST_TITLE_PUBLISHED,
    TEST_TITLE_DRAFT,
    TEST_TITLE_OLD,
    TEST_TITLE_RELATED,
    TEST_PREVIEW,
    TEST_CONTENT,
    TEST_CONTENT_OLD,
    TEST_IMAGE,
    TEST_IMAGE_DRAFT,
    TEST_IMAGE_OLD,
    TEST_IMAGE_RELATED,
    TEST_IMAGE_MAIN,
    TEST_IMAGE_HTML,
    TEST_SESSION_KEY_1,
    TEST_SESSION_KEY_2,
    TEST_TAG,
    TEST_INVALID_SHORT_TITLE,
    TEST_INVALID_DIGITS_TITLE,
)
from blog.constants import MAX_LENGTH_STR


pytestmark = pytest.mark.django_db


# =================================================
# FIXTURES
# =================================================

@pytest.fixture
def published_post():
    """Опубликованный пост."""
    return Post.objects.create(
        title=TEST_TITLE_PUBLISHED,
        preview=TEST_PREVIEW,
        content=TEST_CONTENT,
        image=TEST_IMAGE,
        status=Post.Status.PUBLISHED,
    )


@pytest.fixture
def draft_post():
    """Черновик поста."""
    return Post.objects.create(
        title=TEST_TITLE_DRAFT,
        content=TEST_CONTENT,
        image=TEST_IMAGE_DRAFT,
        status=Post.Status.DRAFT,
    )


# =================================================
# MODELS: Post, PostView
# =================================================

def test_post_str_truncated(published_post):
    """Метод __str__ возвращает укороченный заголовок."""
    assert str(published_post) == published_post.title[:MAX_LENGTH_STR]


def test_get_absolute_url_contains_slug(published_post):
    """get_absolute_url содержит slug поста."""
    url = published_post.get_absolute_url()
    assert published_post.slug in url


def test_views_count(published_post):
    """Метод views_count корректно считает просмотры."""
    PostView.objects.create(
        post=published_post, session_key=TEST_SESSION_KEY_1
    )
    PostView.objects.create(
        post=published_post, session_key=TEST_SESSION_KEY_2
    )

    assert published_post.views_count() == 2


# =================================================
# MANAGER: PublishedManager
# =================================================

def test_published_manager_returns_only_published(
    published_post, draft_post
):
    """Менеджер published возвращает только опубликованные посты."""
    posts = Post.published.all()

    assert published_post in posts
    assert draft_post not in posts
    assert posts.count() == 1


# =================================================
# MODEL METHODS: recent / related posts
# =================================================

def test_get_recent_posts_excludes_current(published_post):
    """Метод get_recent_posts исключает текущий пост."""
    older_post = Post.objects.create(
        title=TEST_TITLE_OLD,
        content=TEST_CONTENT_OLD,
        image=TEST_IMAGE_OLD,
        status=Post.Status.PUBLISHED,
    )

    recent_posts = published_post.get_recent_posts()

    assert published_post not in recent_posts
    assert older_post in recent_posts


def test_get_related_posts_by_tags(published_post):
    """Метод get_related_posts возвращает посты с общими тегами."""
    related_post = Post.objects.create(
        title=TEST_TITLE_RELATED,
        content=TEST_CONTENT,
        image=TEST_IMAGE_RELATED,
        status=Post.Status.PUBLISHED,
    )

    published_post.tags.add(TEST_TAG)
    related_post.tags.add(TEST_TAG)

    related_posts = published_post.get_related_posts()

    assert related_post in related_posts


# =================================================
# SERVICES
# =================================================

def test_add_post_view_creates_unique_view(published_post):
    """Один session_key создаёт только один просмотр."""
    add_post_view(published_post, TEST_SESSION_KEY_1)
    add_post_view(published_post, TEST_SESSION_KEY_1)

    assert PostView.objects.count() == 1


# =================================================
# VALIDATORS
# =================================================

def test_validate_title_ok():
    """Корректный заголовок проходит валидацию."""
    validate_title(TEST_TITLE_PUBLISHED)


def test_validate_title_too_short():
    """Слишком короткий заголовок вызывает ValidationError."""
    with pytest.raises(ValidationError):
        validate_title(TEST_INVALID_SHORT_TITLE)


def test_validate_title_only_digits():
    """Заголовок только из цифр вызывает ValidationError."""
    with pytest.raises(ValidationError):
        validate_title(TEST_INVALID_DIGITS_TITLE)


# =================================================
# VIEWS
# =================================================

def test_post_list_view_returns_published(
    client, published_post, draft_post
):
    """ListView возвращает только опубликованные посты."""
    url = reverse("blog:post_list")
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert published_post in response.context["posts"]
    assert draft_post not in response.context["posts"]


def test_post_detail_view_adds_view(client, published_post):
    """DetailView добавляет просмотр поста."""
    url = reverse(
        "blog:post_detail", kwargs={"slug": published_post.slug}
    )

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert PostView.objects.filter(post=published_post).exists()


# =================================================
# SIGNALS
# =================================================

@patch("os.remove")
@patch("os.path.isfile", return_value=True)
def test_delete_post_images_signal(mock_isfile, mock_remove):
    """Сигнал удаляет изображения поста при его удалении."""
    post = Post.objects.create(
        title=TEST_TITLE_PUBLISHED,
        content=TEST_IMAGE_HTML,
        image=TEST_IMAGE_MAIN,
        status=Post.Status.PUBLISHED,
    )

    post.delete()

    assert mock_remove.called
