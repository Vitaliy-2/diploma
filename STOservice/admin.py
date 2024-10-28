from django.contrib import admin
from .models import Visit, Section, Service, Employee


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'number_plate', 'created_at', 'status', 'section',)
    list_filter = ('status', 'created_at', 'updated_at')
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


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'section', 'hire_date', 'phone', 'is_active')
    list_filter = ('section', 'position', 'is_active')
    search_fields = ('last_name', 'first_name', 'phone')