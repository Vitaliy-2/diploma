from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, TemplateView, View, ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from .models import Note
from .forms import CustomLoginForm, CustomUserCreationForm, CustomPasswordChangeForm, NoteForm




class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    
    def get_success_url(self):
        """
        Когда вью авторизации авторизует пользователя, происходит перенаправление на страницу, указанную
        в  параметре "next" в запросе. Если такой параметр не указан, то происходит перенаправление на домашнюю страницу
        """
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        return next_url or reverse_lazy('main')


def logout_view(request):
    logout(request)
    return redirect('main')


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'password_change.html'
    extra_context = {'title': 'Изменение пароля', 'active_tab': 'password_change'}
    success_url = reverse_lazy('password_change_done')


class CustomPasswordChangeDoneView(TemplateView):
    template_name = 'password_change_done.html'


class ProfileClassView(LoginRequiredMixin, View):
    def post(self, request):
        return render(request, 'profile.html')


class AddNoteView(LoginRequiredMixin, CreateView):
    form_class = NoteForm
    template_name = 'add_note.html'
    success_url = reverse_lazy('my_notes')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Запись успешно добавлена!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'add_note'
        context['title'] = 'Добавить заметку'
        return context


class MyNotesView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'my_notes.html'
    context_object_name = 'note'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'my_notes'
        context['title'] = 'Мои заметки'
        return context
