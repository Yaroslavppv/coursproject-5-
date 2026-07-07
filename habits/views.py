from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.permissions import IsOwnerOrReadOnlyPublic

# Create your views here.
class HabitPagination(PageNumberPagination):
    """Кастомная пагинация: выводим ровно по 5 привычек на страницу"""
    default_limit = 5
    max_limit = 5

class HabitListAPIView(ListAPIView):
    """Список привычек текущего пользователя с пагинацией по 5 штук"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

class HabitPublicListAPIView(ListAPIView):
    """Список всех публичных привычек в системе с пагинацией по 5 штук"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination
    queryset = Habit.objects.filter(is_public=True)

class HabitCreateAPIView(CreateAPIView):
    """Создание новой привычки"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HabitDetailAPIView(RetrieveUpdateDestroyAPIView):
    """Просмотр, детальное/частичное редактирование и удаление конкретной привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyPublic]