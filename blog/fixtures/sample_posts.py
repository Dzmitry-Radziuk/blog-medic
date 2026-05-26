import os
import sys

import django
from django.core.files import File
from django.utils import timezone

# --- 1. Добавляем корень проекта в sys.path ---
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(BASE_DIR)

# --- 2. Настраиваем Django ---
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'config.settings'
)  # <-- твой settings
django.setup()  # <--- обязательно вызвать перед импортом моделей

# --- 3. Импортируем модели ---
from blog.models import Post

# --- 4. Папка с картинками ---
IMAGE_DIR = os.path.join(
    BASE_DIR, 'media', 'posts'
)  # все файлы hero и контентные

# --- 5. Данные статей ---
sample_posts = [
    {
    },
]

# --- 6. Сохраняем посты ---
for post_data in sample_posts:
    image_name = post_data.pop("image", None)
    post, created = Post.objects.update_or_create(
        slug=post_data["slug"], defaults=post_data
    )
    if image_name:
        image_path = os.path.join(IMAGE_DIR, image_name)
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                post.image.save(image_name, File(f), save=True)
        else:
            print(f"Файл {image_path} не найден!")

print("Фикстуры успешно загружены!")
