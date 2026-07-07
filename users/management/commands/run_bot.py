import requests
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Запуск Telegram-бота для получения и автоматической привязки Chat ID"

    def handle(self, *args, **options):
        token = settings.TELEGRAM_BOT_TOKEN
        if not token or "ВАШ_ТОКЕН" in token or "1234567890" in token:
            self.stderr.write("Ошибка: Укажите корректный TELEGRAM_BOT_TOKEN в файле .env")
            return

        self.stdout.write("Telegram-бот успешно запущен и ожидает сообщений...")
        offset = 0
        url = f"https://api.telegram-proxy.org/bot{token}/"

        while True:
            try:
                response = requests.get(f"{url}getUpdates", params={"offset": offset, "timeout": 10}, timeout=15).json()

                if not response.get("result"):
                    continue

                for update in response["result"]:
                    offset = update["update_id"] + 1
                    message = update.get("message")
                    if not message:
                        continue

                    chat_id = message["chat"]["id"]
                    text = message.get("text", "").strip()

                    if text.startswith("/start"):
                        reply = (
                            f"Привет! Твой Telegram Chat ID: `{chat_id}`\n\n"
                            f"Ты можешь скопировать его и указать в личном кабинете на фронтенде.\n"
                            f"Либо отправь мне свой **Email**, с которым ты регистрировался на сайте, "
                            f"и я привяжу уведомления автоматически!"
                        )
                    elif "@" in text:
                        User = get_user_model()
                        user = User.objects.filter(email=text).first()
                        if user:
                            user.telegram_chat_id = chat_id
                            user.save()
                            reply = f"✅ Успешно! Аккаунт **{user.email}** привязан к этому чату. Теперь сюда будут приходить напоминания о привычках."
                        else:
                            reply = f"❌ Пользователь с Email `{text}` не найден в системе трекера привычек."
                    else:
                        reply = "Пожалуйста, отправьте ваш Email для привязки аккаунта или введите команду /start."

                    requests.post(f"{url}sendMessage", json={
                        "chat_id": chat_id,
                        "text": reply,
                        "parse_mode": "Markdown"
                    }, timeout=5)

            except Exception as e:
                self.stdout.write(f"Предупреждение (бот продолжает работу): {e}")
                time.sleep(3)
