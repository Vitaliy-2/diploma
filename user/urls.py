from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .views import (
    logout_view,
    CustomLoginView,
    CustomRegisterView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
    ProfileClassView,
    # CabinetClassView,
    ProfileDataView,
    AddNoteView,
    MyNotesView,
)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    # Смена пароля
    path("password_change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", CustomPasswordChangeDoneView.as_view(), name="password_change_done"),

    # Маршруты восстановления пароля
    # Маршрут для сброса пароля
    path("password-reset/", auth_views.PasswordResetView.as_view(
            template_name="password_reset_form.html",
            email_template_name="password_reset_email.html",
            success_url=reverse_lazy("password_reset_done"),),
        name="password_reset",),

    # Маршрут для подтверждения сброса пароля
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"), name="password_reset_done",),

    # Маршрут для ввода нового пароля
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),),
        name="password_reset_confirm",),

    # Маршрут для завершения сброса пароля
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ), name="password_reset_complete",),
    
    # Личный кабинет
    path("profile/", ProfileClassView.as_view(), name="profile"),

    # Личный кабинет
    # path("cabinet/", CabinetClassView.as_view(), name="cabinet"),

    # Данные пользователя в профиле
    path('profile-data/', ProfileDataView.as_view(), name='profile_data'),

    # Добавление заметки
    path('add-work-record/', AddNoteView.as_view(), name='add_note'),
    # Список заметок
    path('my-notes/', MyNotesView.as_view(), name='my_notes'),
]
