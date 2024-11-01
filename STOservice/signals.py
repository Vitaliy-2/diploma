from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Visit, Review
from .telegram_bot import send_telegram_message
from STO.settings import TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID
import asyncio


@receiver(m2m_changed, sender=Visit.services.through)
def send_telegram_notification(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для модели Visit.
    Он обрабатывает добавление КАЖДОЙ услуги в запись на обслуживание.
    Отправка ОДНОГО сообщения в телеграмм выполняется в первом условии
    """
    if action == 'post_add' and kwargs.get('pk_set'):
        services = [service.name for service in instance.services.all()]
        print(f"УСЛУГИ: {services}")
        message = f"""
*Новая запись на обслуживание* 

*Имя:* {instance.name} 
*Телефон:* {instance.phone or 'не указан'}
*Марка:* {instance.brand or 'не указан'} 
*Номер:* {instance.number_plate or 'не указан'} 
*Комментарий:* {instance.comment or 'не указан'}
*Раздел:* {instance.section.name}
*Услуги:* {', '.join(services) or 'не указаны'}
-------------------------------------------------------------
"""
        asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))


@receiver(post_save, sender=Review)
def send_review_telegram_notification(sender, instance, created, **kwargs):
    if created:
        message = "*Новый отзыв на сайте*"
        asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))