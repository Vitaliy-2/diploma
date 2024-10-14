from django.contrib import admin
from django.urls import path

from django.conf.urls import include


from STOservice.views import (
    MainView,
    AboutView,
    ServicesView,
#     VisitFormView,
#     ThanksTemplateView,
#     ServicesBySectionView,
#     VisitCreateView,
#     VisitDetailView,
#     VisitUpdateView,
#     VisitDeleteView,
#     VisitListView,
)

# from user import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
]
