from django.db import models
from django.contrib.auth import get_user_model

class Note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='work_records')
    car_brand = models.CharField(max_length=100, verbose_name='Марка автомобиля')
    mileage = models.IntegerField(verbose_name='Пробег')
    work_done = models.TextField(verbose_name='Проделанные работы')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_brand} - {self.work_done}"

