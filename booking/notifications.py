from django.core.mail import send_mail
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

def send_booking_confirmation_email(booking):
    """Отправка email-уведомления о бронировании"""
    subject = f'Подтверждение бронирования: {booking.event.title}'
    message = f'''
    Здравствуйте, {booking.user_name}!
    
    Спасибо за бронирование мероприятия "{booking.event.title}".
    
    Детали бронирования:
    Дата: {booking.event.event_date}
    Время: {booking.event.start_time}
    Место: {booking.event.location.name}, {booking.event.location.address}
    
    Мы свяжемся с вами для подтверждения бронирования.
    
    С уважением,
    Команда Bronirov
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user_email],
            fail_silently=False,
        )
        logger.info(f'Email sent successfully to {booking.user_email}')
    except Exception as e:
        logger.error(f'Failed to send email: {str(e)}')

def send_telegram_notification(booking):
    """Отправка уведомления в Telegram"""
    if not booking.user_telegram:
        return
        
    message = f'''
    🎫 Новое бронирование!
    
    Мероприятие: {booking.event.title}
    Клиент: {booking.user_name}
    Email: {booking.user_email}
    Telegram: {booking.user_telegram}
    
    Дата: {booking.event.event_date}
    Время: {booking.event.start_time}
    Место: {booking.event.location.name}
    '''
    
    try:
        telegram_api_url = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage'
        data = {
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(telegram_api_url, data=data)
        response.raise_for_status()
        logger.info('Telegram notification sent successfully')
    except Exception as e:
        logger.error(f'Failed to send Telegram notification: {str(e)}') 