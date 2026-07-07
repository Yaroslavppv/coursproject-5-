from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Имя пользователя"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email (Электронная почта)"
    )

    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Telegram Chat ID"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email