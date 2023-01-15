from rest_framework.serializers import ModelSerializer

from bot.models import TgUser


class TgUserSerializer(ModelSerializer):
    class Meta:
        model = TgUser
        fields = ('verification_code',)
