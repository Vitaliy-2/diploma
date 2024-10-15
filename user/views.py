from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, TemplateView, View

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomLoginForm, CustomUserCreationForm, CustomPasswordChangeForm




class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    
    def get_success_url(self):
        """
        Когда вью авторизации авторизует пользователя, происходит перенаправление на страницу, указанную
        в  параметре "next" в запросе. Если такой параметр не указан, то происходит перенаправление на домашнюю страниц
        """
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        return next_url or reverse_lazy('main')


def logout_view(request):
    # logout - выйти из системы
    logout(request)
    return redirect('main')


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change_done')


class CustomPasswordChangeDoneView(TemplateView):
    template_name = 'password_change_done.html'


class CabinetClassView(LoginRequiredMixin, View):
    def post(self, request):
        return render(request, 'cabinet.html')
