from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .views import (
    logout_view,
    CustomLoginView,
    CustomRegisterView,
)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
]
