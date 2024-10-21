from django.contrib import admin
from .models import Note

admin.site.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_brand', 'mileage', 'work_done', 'amount', 'created_at',)
    list_filter = ('user', 'car_brand', 'created_at')
    search_fields = ('user', 'car_brand')