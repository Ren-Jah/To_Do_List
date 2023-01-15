from django.db import models
from django.utils.crypto import get_random_string


# TgUser
class TgUser(models.Model):
    class Meta:
        verbose_name = "Tg пользователь"
        verbose_name_plural = "Tg пользователи"

    tg_chat_id = models.BigIntegerField()
    tg_user_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(
        'core.User', verbose_name="Автор", on_delete=models.PROTECT, null=True
    )
    verification_code = models.CharField(max_length=10, unique=True)

    def generate_verification_code(self) -> str:
        code = get_random_string(10)
        self.verification_code = code
        self.save()
        return code
