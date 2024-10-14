from django.db import models

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
    vin = models.CharField(max_length=17, blank=True, verbose_name='vin')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
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
    # section = models.ForeignKey('Section', on_delete=models.CASCADE, verbose_name='Раздел')  # Связь с разделом

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
