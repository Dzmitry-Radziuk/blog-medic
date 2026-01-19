from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from taggit.models import Tag

from .models import Post
from .validators import validate_title


class PostAdminForm(forms.ModelForm):
    """Форма для админки поста с CKEditor и выбором тегов."""

    content = forms.CharField(widget=CKEditorUploadingWidget())
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple(
            verbose_name='Теги', is_stacked=False
        ),
    )

    class Meta:
        """Метаданные формы PostAdminForm."""

        model = Post
        fields = '__all__'

    def clean_title(self):
        """Валидация поля title: не менее 3 символов и не только цифры."""
        title = self.cleaned_data.get('title', '')
        validate_title(title)
        return title

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы: выставляем
        выбранные теги для существующего поста.
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = [
                t.pk for t in self.instance.tags.all()
            ]

    def save(self, commit=True):
        """Сохраняет пост и применяет выбранные теги."""
        instance = super().save(commit=commit)
        if commit:
            instance.tags.set(self.cleaned_data.get('tags', []))
        else:
            self._tags_to_set = self.cleaned_data.get('tags', [])
        return instance

    def save_m2m(self):
        """Применяем отложенные теги после сохранения модели."""
        super().save_m2m()
        if hasattr(self, '_tags_to_set'):
            self.instance.tags.set(self._tags_to_set)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройка отображения модели Post в админке."""

    form: type[PostAdminForm] = PostAdminForm
    list_display: tuple = ('title', 'status', 'created_at', 'get_tags')
    search_fields: tuple = ('title', 'preview', 'content', 'tags__name')
    list_filter: tuple = ('status', 'created_at', 'tags')

    def get_tags(self, obj: Post) -> str:
        """Возвращает строку с тегами для отображения в списке."""
        return ', '.join(tag.name for tag in obj.tags.all())

    get_tags.short_description = 'Теги'
