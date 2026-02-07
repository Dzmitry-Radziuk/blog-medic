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
        "title": "Как распознать мигрень",
        "slug": "migren-raspoznavanie",
        "preview": "Мигрень — это не просто головная боль...",
        "content": """
        <p>Мигрень — это неврологическое заболевание...</p>
        <img src="/media/posts/migren_brain.jpg" alt="Мигрень">
        """,
        "image": "migren_hero.jpg",
        "status": "published",
        "created_at": timezone.now(),
    },
    {
        "title": "Влияние сна на работу нервной системы",
        "slug": "son-i-nervnaya-sistema",
        "preview": "Сон критически важен для здоровья мозга и нервной системы. Узнайте, как недосып влияет на когнитивные функции.",
        "content": """
        <p>Во время сна происходит восстановление нейронных связей и очистка мозга от токсинов.</p>
        <img src="/media/posts/sleep_brain.jpg" alt="Сон и мозг" style="max-width:100%; margin:10px 0;">
        <p>Хронический недосып может приводить к снижению памяти, внимательности и повышенной тревожности.</p>
        """,
        "image": "sleep_hero.jpg",
        "status": "published",
        "created_at": timezone.now(),
    },
    {
        "title": "Реабилитация после инсульта: важные этапы",
        "slug": "reabilitatsiya-posle-insulta",
        "preview": "После инсульта начинается сложный процесс восстановления. Рассмотрим ключевые этапы и методы реабилитации.",
        "content": """
        <p>Реабилитация включает восстановление моторики, речи и когнитивных функций.</p>
        <img src="/media/posts/stroke_rehab.jpg" alt="Реабилитация после инсульта" style="max-width:100%; margin:10px 0;">
        <p>Важна индивидуальная программа, составленная врачом-неврологом и физиотерапевтом.</p>
        """,
        "image": "rehab_hero.jpg",
        "status": "published",
        "created_at": timezone.now(),
    },
    {
        "title": "Боль в спине: причины и профилактика",
        "slug": "bol-v-spine",
        "preview": "Боль в спине встречается почти у каждого. Разберем основные причины и способы предотвращения проблем.",
        "content": """
        <p>Основные причины боли в спине: неправильная осанка, сидячий образ жизни, травмы и остеохондроз.</p>
        <img src="/media/posts/back_pain.jpg" alt="Боль в спине" style="max-width:100%; margin:10px 0;">
        <p>Профилактика: укрепление мышц, упражнения на растяжку, регулярные перерывы при сидячей работе.</p>
        """,
        "image": "back_hero.jpg",
        "status": "published",
        "created_at": timezone.now(),
    },
    {
        "title": "Стресс и нервная система: влияние и советы",
        "slug": "stress-i-nervnaya-sistema",
        "preview": "Стресс оказывает прямое влияние на работу мозга и нервной системы. Узнайте, как защитить себя.",
        "content": """
        <p>Хронический стресс вызывает напряжение мышц, головные боли и нарушения сна. Стресс — это естественная реакция организма на вызовы или угрозы, проявляющаяся как физическим, так, и умственным напряжением, помогающая мобилизовать силы (реакция «бей или беги»), но длительный или чрезмерный стресс вреден для здоровья, вызывая усталость, раздражительность, проблемы со сном, концентрацией и пищеварением, и требует управления через отдых, спорт, здоровое питание, а в случае трудностей — обращения за помощью.</p>
        <img src="/media/posts/stress.jpg" alt="Стресс и мозг" style="max-width:100%; margin:10px 0;">
        <p>Советы: медитация, дыхательные упражнения, прогулки на свежем воздухе, правильное питание.</p>
        """,
        "image": "stress_hero.jpg",
        "status": "published",
        "created_at": timezone.now(),
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
