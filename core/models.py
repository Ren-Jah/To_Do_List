from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Класс пользователя наследуемый от AbstractUser """
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
