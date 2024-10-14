from django.contrib import admin
from .models import Visit, Section, Service


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'vin', 'created_at', 'status', 'section',)
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'comment')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('services',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name', 'description')
    # list_filter = ('section',)  # Фильтрация по услугам