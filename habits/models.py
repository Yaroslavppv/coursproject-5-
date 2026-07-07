from django.db import models
from django.conf import settings

# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        related_name="habits"
    )

    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        related_name="linked_to"
    )

    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность (в днях)")
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")
    duration = models.PositiveIntegerField(default=60, verbose_name="Время на выполнение (в секундах)")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['id']

    def __str__(self):
        return f"{self.action} в {self.time} ({self.place})"