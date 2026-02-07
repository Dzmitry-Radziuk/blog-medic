from operator import itemgetter

from django.views.generic import TemplateView

from .data import COURSES, EDUCATION, YEAR


class BasePageView(TemplateView):
    """Базовое представление для страниц, чтобы не дублировать год."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = YEAR
        return context


class HomePageView(BasePageView):
    """Представление домашней страницы."""

    template_name = 'pages/home.html'


class AboutPageView(BasePageView):
    """Представление страницы - О враче."""

    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['education'] = sorted(EDUCATION, key=itemgetter('year'))
        context['courses'] = sorted(COURSES, key=itemgetter('year'))
        return context


class ContactPageView(BasePageView):
    """Представление страницы - Контакты."""

    template_name = 'pages/contact.html'
