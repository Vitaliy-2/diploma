from django.contrib import admin
from django.urls import path

from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from STOservice.views import (
    MainView,
    AboutView,
    ServicesView,
    VisitFormView,
    ThanksTemplateView,
    ServicesBySectionView,
    VisitCreateView,
    VisitDetailView,
    VisitUpdateView,
    VisitDeleteView,
    VisitListView,
    ReviewCreateView
)

from user import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
    path('appointment/', VisitFormView.as_view(), name='appointment'),
    path('thanks/', ThanksTemplateView.as_view(), name='thanks'),
    path('review/', ReviewCreateView.as_view(), name='review'),

    # Маршрут для скрипта
    path("get_services_by_section/<int:section_id>/", ServicesBySectionView.as_view(), name="get_services_by_section"),

    # CRUD для Visit 
    path('visit/add/', VisitCreateView.as_view(), name='visit-form'),
    path("visit/<int:pk>/view/", VisitDetailView.as_view(), name="visit-view"),
    path("visit/<int:pk>/edit/", VisitUpdateView.as_view(), name="visit-edit"),
    path("visit/<int:pk>/delete/", VisitDeleteView.as_view(), name="visit-delete"),
    path("visits/", VisitListView.as_view(), name="visits"),

    # Подключение пользователей с префиксом user
    path("user/", include(urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
