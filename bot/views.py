from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class BotVerifyView(GenericAPIView):
    """ Вьюшка для привязки телеграмм-бота"""
    model = TgUser
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        """ Метод для привязки телеграмм-бота"""
        data = self.serializer_class(request.data).data
        tg_client = TgClient("5987351996:AAHn5lnwAgMi2uooEYKuzMD3pii-F6CYCAE")
        tg_user = TgUser.objects.first(verification_code=data['verification_code']).first
        if not tg_user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        tg_user.user = request.user
        tg_user.save()
        tg_client.send_message(
            chat_id=tg_user.tg_chat.id,
            text='Успешно'
        )
        return Response(data=data, status=status.HTTP_201_CREATED)
