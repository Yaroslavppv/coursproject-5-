from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from habits.models import Habit

# Create your tests here.
class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            username="testuser",
            password="testpassword123"
        )
        self.client.force_authenticate(user=self.user)

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Выпить кофе",
            is_pleasant=True,
            periodicity=1,
            duration=30
        )

    def test_create_habit_success(self):
        """Тест успешного создания полезной привычки"""
        url = reverse('habit_create')
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Пробежка",
            "is_pleasant": False,
            "periodicity": 1,
            "duration": 60,
            "reward": "Съесть фрукт"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(action="Пробежка").count(), 1)

    def test_validator_duration_error(self):
        """Тест валидатора: время выполнения не больше 120 секунд"""
        url = reverse('habit_create')
        data = {
            "place": "Зал",
            "time": "12:00:00",
            "action": "Тренировка",
            "duration": 150,
            "periodicity": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validator_reward_and_related_habit_error(self):
        """Тест валидатора: нельзя одновременно указывать награду и связанную привычку"""
        url = reverse('habit_create')
        data = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Чтение книги",
            "related_habit": self.pleasant_habit.id,
            "reward": "Шоколадка",
            "duration": 60,
            "periodicity": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validator_periodicity_error(self):
        """Тест валидатора: периодичность не реже 1 раза в 7 дней"""
        url = reverse('habit_create')
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Уборка",
            "periodicity": 10,
            "duration": 60
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_habit_list(self):
        """Тест получения списка привычек пользователя"""
        url = reverse('habit_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) >= 1)