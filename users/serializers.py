from rest_framework import serializers
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'password', 'telegram_chat_id')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', ''),
            password=validated_data['password'],
            telegram_chat_id=validated_data.get('telegram_chat_id')
        )
        return user
