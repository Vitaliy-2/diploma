from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .views import (
    logout_view,
    CustomLoginView,
    CustomRegisterView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    # Смена пароля
    path("password_change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
]
