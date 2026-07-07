from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Настройка отображения полей в админке
    model = User
    list_display = ('email', 'username', 'telegram_chat_id', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Telegram инфо', {'fields': ('telegram_chat_id',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Telegram info', {'fields': ('telegram_chat_id',)}),
    )