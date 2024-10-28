from django.apps import AppConfig


class StoserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'STOservice'
    verbose_name = 'Записи клиентов'

    # По готовности приложения будет импортирован сигнал
    # def ready(self):
    #     import STOservice.signals
