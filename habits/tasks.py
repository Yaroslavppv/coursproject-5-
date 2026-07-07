import requests
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from habits.models import Habit


@shared_task
def send_habit_reminders():
    now_time = timezone.localtime().time().strftime('%H:%M')
    habits = Habit.objects.filter(user__telegram_chat_id__isnull=False)

    for habit in habits:
        if habit.time.strftime('%H:%M') == now_time:
            chat_id = habit.user.telegram_chat_id

            message = f"⏰ **Напоминание о привычке!**\n\n"
            message += f"Я буду **{habit.action}** в **{now_time}** в **{habit.place}**.\n"
            message += f"⏱ _Время на выполнение:_ {habit.duration} сек.\n"

            if habit.related_habit:
                message += f"🎉 **Вознаграждение после:** {habit.related_habit.action}"
            elif habit.reward:
                message += f"🎁 **Вознаграждение после:** {habit.reward}"

            url = f"https://api.telegram-proxy.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }

            try:
                response = requests.post(url, json=payload, timeout=5)
                if response.status_code != 200:
                    print(f"Ошибка TG API для chat_id {chat_id}: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка сети при отправке уведомления для chat_id {chat_id}: {e}")
