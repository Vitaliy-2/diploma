from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.db.models import Q

from django.http import JsonResponse

from django.views.generic import (
    TemplateView,
    # FormView,
    # View,
    # CreateView,
    # DetailView,
    # UpdateView,
    # ListView,
    # DeleteView,
)

# Для ограничения доступа неавторизованных пользователей
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# from .forms import VisitModelForm, VisitEditModelForm
# from .models import Visit, Section


MENU = [
        {'title': 'Главная', 'url': '/', 'alias': 'main'},
        {'title': 'О сервисе', 'url': '/about/', 'alias': 'about'},
        {'title': 'Услуги', 'url': '/services/', 'alias': 'services'},
        {'title': 'Отзывы', 'url': '#reviews', 'alias': True},
        {'title': 'Запись', 'url': '/appointment/', 'alias': 'appointment'},
    ]


def get_menu_context(menu: list[dict] = MENU):
    return {"menu": menu}


class MainView(TemplateView):
    template_name = "main.html"

    # Расширяем метод. Добавляем контекст ключ - меню.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        context.update({'page_alias': 'main'})
        return context


class AboutView(TemplateView):
    template_name = "about.html"

    # Расширяем метод. Добавляем контекст ключ - меню.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        context.update({'page_alias': 'about'})
        return context


class ServicesView(TemplateView):
    template_name = "services.html"

    # Расширяем метод. Добавляем контекст ключ - меню.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        context.update({'page_alias': 'services'})
        return context