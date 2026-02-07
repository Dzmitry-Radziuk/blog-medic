from django.db.models import Count
from django.views.generic import DetailView, ListView

from .models import Post
from .services import add_post_view
from .utils import get_session_key


class PostListView(ListView):
    """Список опубликованных постов с подсчетом просмотров."""

    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.published.annotate(
        views_total=Count('views', distinct=True)
    ).order_by('-created_at')


class PostDetailView(DetailView):
    """
    Детальная страница поста с добавлением
    просмотра и дополнительным контекстом.
    """

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    queryset = Post.published.prefetch_related('tags')

    def get(self, request, *args, **kwargs):
        """Обрабатывает GET-запрос и регистрирует просмотр поста."""
        response = super().get(request, *args, **kwargs)
        session_key = get_session_key(request)
        add_post_view(self.object, session_key)
        return response

    def get_context_data(self, **kwargs):
        """Добавляет в контекст последние и похожие посты."""
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = self.object.get_recent_posts()
        context['related_posts'] = self.object.get_related_posts()
        return context
