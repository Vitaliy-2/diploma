from django.db import models
from django.template.defaultfilters import date as date_filter

# Класс для записи на обслуживание авто
class Visit(models.Model):

    STATUS_CHOICES = [
        (0, 'Не подтверждена'),
        (1, 'Подтверждена'),
        (2, 'Отменена'),
        (3, 'Выполнена'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    brand = models.CharField(max_length=100, verbose_name='Марка автомобиля')
    number_plate = models.CharField(max_length=6, verbose_name='Номер автомобиля')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='Статус')
    
    section = models.ForeignKey('Section', on_delete=models.CASCADE, verbose_name='Раздел')
    services = models.ManyToManyField('Service', verbose_name='Услуги')

    def __str__(self):
        return f'{self.name} - {self.phone}'
    
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"


# Класс для разделов
class Section(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    services = models.ManyToManyField('Service', related_name='sections', verbose_name='Услуги')

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"


# Класс для услуг
class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


# Класс для сотрудников
class Employee(models.Model):
    image = models.ImageField(upload_to='employees/', verbose_name='Фото', null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    position = models.CharField(max_length=100, verbose_name='Должность')
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, verbose_name='Раздел')
    hire_date = models.DateField(verbose_name='Дата приема на работу')
    is_active = models.BooleanField(default=True, verbose_name='Работает')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    

class Review(models.Model):
    STATUS_CHOICES = [
        (0, 'Не проверен'),
        (1, 'Проверен'),
    ]

    name = models.CharField(max_length=100, verbose_name="Имя")
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models. IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='Статус')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.name} ({date_filter(self.created_at, "d.m.Y")})'
