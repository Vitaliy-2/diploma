from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.db.models import Q

from django.http import JsonResponse

from django.views.generic import (
    TemplateView,
    FormView,
    View,
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView,
)

# Для ограничения доступа неавторизованных пользователей
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import VisitModelForm, VisitEditModelForm
from .models import Visit, Section
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import UserPassesTestMixin



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
    

# класс для отображения форм
class VisitFormView(FormView):
    template_name = "visit_form.html"
    form_class = VisitModelForm
    success_url = "/thanks/"
    # context = get_menu_context()

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    # Расширяем метод. Добавляем контекст ключ - меню.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        context.update({'page_alias': 'appointment'})
        return context


# Используется для статичных страниц, где данные особо не меняются
class ThanksTemplateView(TemplateView):
    template_name = "thanks.html"
    
    # Расширяем метод. Добавляем контекст ключ - меню.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        return context


class ServicesBySectionView(View):
    
    def get(self, request, section_id):
        services = Section.objects.get(id=section_id).services.all()
        services_data = [
            {"id": service.id, "name": service.name} for service in services
        ]
        return JsonResponse({"services": services_data})
    

class VisitCreateView(CreateView):
    template_name = "visit_form.html"
    model = Visit
    # fields = ["name", "phone", "comment", "master", "services"] # Мы можем обойтись даже без формы!!!
    form_class = VisitModelForm
    # Подтянем url по псевдониму thanks\
    # Функция для поиска маршрутов по имени (надежный метод)
    success_url = reverse_lazy("thanks")\


class VisitUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'STOservice.change_visit'
    template_name = "visit_form.html"
    model = Visit
    # fields = ["name", "phone", "comment", "master", "services"] # Мы можем обойтись даже без формы!!!
    form_class = VisitEditModelForm
    # Подтянем url по псевдониму thanks\
    # Функция для поиска маршрутов по имени (надежный метод)
    success_url = reverse_lazy("thanks")


# Миксин, дает проверку прав, выдаваемых через админку PermissionRequiredMixin, 
class VisitDetailView(PermissionRequiredMixin, DetailView):
    # Где core - приложение, view - право доступа на одну из круд операцию, visit - модель
    permission_required = 'STOservice.view_visit'
    # raise_exception = True
    template_name = "visit_detail.html"
    model = Visit
    # Переменная в которую поместятся данные об объекте, из которой можно вытягивать данные в шаблон
    context_object_name = "visit"


class VisitDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'STOservice.delete_visit'
    template_name = "visit_confirm_delete.html"
    model = Visit
    success_url = reverse_lazy("thanks")


class VisitListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "visit_list.html"
    model = Visit
    context_object_name = "visits"
    paginate_by = 5

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists() or self.request.user.is_superuser

    def get_queryset(self):
        """
        Расширили служебный метод get_queryset()
        Который поставляет в контекст шаблона список записей
        """
        # Используя родителя получили все
        queryset = super().get_queryset()
        
        # Добыли поисковый запрос \ или None
        search_query = self.request.GET.get('search')
        
        # Если поисковый запрос есть, то фильтруем
        if search_query:
            queryset = queryset.filter(
                Q(name__iregex=search_query) | Q(phone__icontains=search_query)
            )
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """
        Расширяем служебный метод get_context_data()
        Для передачи в контекст шаблона дополнительных данных
        касательно поисковой строки
        """
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search')
        if search_query:
            context['search'] = search_query
        return context


class Custom403View(TemplateView):
    template_name = '403.html'
    status_code = 403


class Custom404View(TemplateView):
    template_name = '404.html'
    status_code = 404
