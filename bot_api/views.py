from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from users.models import TelegramConfirmation, UserProfile
import json

# Create your views here.

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message', {})
        text = message.get('text', '')
        chat = message.get('chat', {})
        chat_id = str(chat.get('id'))
        if text.startswith('/start '):
            token = text.split(' ', 1)[1].strip()
            try:
                confirmation = TelegramConfirmation.objects.get(token=token, is_confirmed=False)
                profile = confirmation.user.profile
                profile.telegram_chat_id = chat_id
                profile.is_telegram_verified = True
                profile.save()
                confirmation.mark_confirmed()
                return JsonResponse({'ok': True, 'message': '✅ Telegram подтверждён!'} )
            except TelegramConfirmation.DoesNotExist:
                return JsonResponse({'ok': False, 'message': '❌ Токен не найден или уже подтверждён.'})
        return JsonResponse({'ok': False, 'message': 'Неверная команда.'})
    return JsonResponse({'ok': False, 'message': 'Только POST.'})
