from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.text import Truncator
from slugify import slugify
from taggit.managers import TaggableManager

from . import constants
from .validators import validate_title


class PublishedManager(models.Manager):
    'Менеджер для получения только опубликованных постов.'

    def get_queryset(self) -> QuerySet['Post']:
        'Возвращает queryset только с опубликованными постами.'
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    'Модель статьи блога.'

    class Status(models.TextChoices):
        'Статусы публикации поста.'

        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликовано'

    title: str = models.CharField(
        max_length=constants.MAX_LENGTH_TITLE,
        verbose_name='Заголовок',
        db_index=True,
        validators=[validate_title],
    )
    slug: str = AutoSlugField(
        populate_from='title',
        unique=True,
        always_update=True,
        slugify=slugify,
        verbose_name='URL',
        help_text='Автоматически генерируется из заголовка',
    )
    preview: str = models.TextField(
        blank=True,
        verbose_name='Краткое описание',
    )
    content: str = RichTextUploadingField(
        verbose_name='Текст статьи',
    )
    image = models.ImageField(
        upload_to='posts/',
        verbose_name='Главное изображение',
    )
    status: str = models.CharField(
        max_length=constants.STATUS_MAX_LENGTH,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус',
        db_index=True,
    )
    tags: TaggableManager = TaggableManager(
        help_text='Теги для статьи',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления', db_index=True
    )

    objects: models.Manager['Post'] = models.Manager()
    published: PublishedManager = PublishedManager()

    class Meta:
        'Метаданные модели Post.'

        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self) -> str:
        'Возвращает укороченный заголовок поста.'
        return Truncator(self.title).chars(constants.MAX_LENGTH_STR)

    def get_absolute_url(self) -> str:
        'Возвращает абсолютный URL страницы поста.'
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_recent_posts(
        self, n: int = constants.DEFAULT_LENGTH_RECENT_POSTS
    ) -> QuerySet['Post']:
        'Возвращает последние опубликованные посты, кроме текущего.'
        return (
            Post.published.exclude(pk=self.pk)
            .order_by('-created_at')
            .prefetch_related('tags')[:n]
        )

    def get_related_posts(
        self, n: int = constants.DEFAULT_LENGTH_RELATED_POSTS
    ) -> QuerySet['Post']:
        'Возвращает похожие посты по тегам, кроме текущего.'
        return (
            Post.published.prefetch_related('tags')
            .filter(tags__in=self.tags.all())
            .exclude(pk=self.pk)
            .distinct()[:n]
        )

    def views_count(self) -> int:
        'Возвращает количество просмотров поста.'
        return self.views.count()


class PostView(models.Model):
    'Модель просмотра поста пользователем.'

    post: Post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='views', db_index=True
    )
    session_key: str = models.CharField(
        max_length=constants.MAX_LENGTH_SESSION_KEY,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        'Метаданные модели PostView.'

        unique_together = ('post', 'session_key')
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]

    def __str__(self) -> str:
        'Возвращает строковое представление просмотра.'
        return (
            f'{Truncator(self.post).chars(constants.MAX_LENGTH_STR)}'
            f'— {Truncator(self.session_key).chars(
                    constants.MAX_LENGTH_STR)}'
        )
