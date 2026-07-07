"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import RegisterView
from habits.views import (
    HabitListAPIView,
    HabitPublicListAPIView,
    HabitCreateAPIView,
    HabitDetailAPIView
)

schema_view = get_schema_view(
   openapi.Info(
      title="Habit Tracker API",
      default_version='v1',
      description="Документация эндпоинтов бэкенда для интеграции с фронтендом трекера привычек",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/habits/', HabitListAPIView.as_view(), name='habit_list'),
    path('api/habits/public/', HabitPublicListAPIView.as_view(), name='habit_public_list'),
    path('api/habits/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('api/habits/<int:pk>/', HabitDetailAPIView.as_view(), name='habit_detail'),
]
