from rest_framework import serializers
from habits.models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, attrs):
        is_pleasant = attrs.get('is_pleasant', getattr(self.instance, 'is_pleasant', False))
        duration = attrs.get('duration', getattr(self.instance, 'duration', 60))
        periodicity = attrs.get('periodicity', getattr(self.instance, 'periodicity', 1))

        reward = attrs.get('reward')
        related_habit = attrs.get('related_habit')

        if self.instance:
            if 'reward' not in attrs:
                reward = self.instance.reward
            if 'related_habit' not in attrs:
                related_habit = self.instance.related_habit

        if related_habit and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно заполнять и поле вознаграждения, и поле связанной привычки."
            )

        if duration > 120:
            raise serializers.ValidationError(
                "Время на выполнение должно быть не более 120 секунд (2 минут)."
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка обязательно должна быть приятной (is_pleasant=True)."
            )

        if is_pleasant:
            if reward or related_habit:
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )

        if periodicity > 7:
            raise serializers.ValidationError(
                "Интервал повторения привычки не может превышать 7 дней (минимум 1 раз в неделю)."
            )

        return attrs
