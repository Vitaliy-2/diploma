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
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import VisitModelForm, VisitEditModelForm, ReviewForm
from .models import Visit, Section, Employee, Review


MENU = [
        {'title': 'Главная', 'url': '/', 'alias': 'main'},
        {'title': 'Об услугах', 'url': '/about/', 'alias': 'about'},
        {'title': 'Галерея услуг', 'url': '/services/', 'alias': 'services'},
        {'title': 'Оставить отзыв', 'url': '/review/', 'alias': 'review'},
        {'title': 'Запись', 'url': '/appointment/', 'alias': 'appointment'},
    ]


def get_menu_context(menu: list[dict] = MENU):
    return {"menu": menu}


class MainView(TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        context.update({'page_alias': 'main'})
        employees = Employee.objects.filter(is_active=True)
        context.update({'employees': employees})
        reviews = Review.objects.filter(status=1)
        context.update({'reviews': reviews})
        return context


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        context.update({'page_alias': 'about'})
        return context


class ServicesView(TemplateView):
    template_name = "services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        context.update({'page_alias': 'services'})
        return context


class VisitFormView(FormView):
    template_name = "visit_form.html"
    form_class = VisitModelForm
    success_url = "/thanks/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        context.update({'page_alias': 'appointment'})
        return context


class ThanksTemplateView(TemplateView):
    template_name = "thanks.html"

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
    form_class = VisitModelForm
    success_url = reverse_lazy("thanks")


class VisitUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'STOservice.change_visit'
    template_name = "visit_form.html"
    model = Visit
    form_class = VisitEditModelForm
    success_url = reverse_lazy("visits")


class VisitDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'STOservice.view_visit'
    template_name = "visit_detail.html"
    model = Visit
    context_object_name = "visit"


class VisitDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'STOservice.delete_visit'
    template_name = "visit_confirm_delete.html"
    model = Visit
    success_url = reverse_lazy("visits")


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
        queryset = super().get_queryset()
        
        # Добыли поисковый запрос \ None
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


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('main')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        context.update({'page_alias': 'review'})
        return context


class Custom403View(TemplateView):
    template_name = '403.html'
    status_code = 403


class Custom404View(TemplateView):
    template_name = '404.html'
    status_code = 404
