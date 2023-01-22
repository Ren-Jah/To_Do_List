from rest_framework.serializers import ModelSerializer

from bot.models import TgUser


class TgUserSerializer(ModelSerializer):
    """ Сериализатор для модели TgUser """
    class Meta:
        model = TgUser
        fields = ('verification_code',)
