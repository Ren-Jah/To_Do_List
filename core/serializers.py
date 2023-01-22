from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.contrib.auth.hashers import make_password

USER_MODEL = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации новых пользователей """
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def create(self, validated_data) -> USER_MODEL:
        """ Метод для создания нового пользователя """
        password = validated_data.get('password')
        password_repeat = validated_data.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError('Пароли не совпадают.')

        try:
            password_validation.validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': e.args[0]})

        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = USER_MODEL
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    """ Сериализатор входа пользователя в аккаунт"""
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = USER_MODEL
        fields = ['username', 'password']

    def validate(self, attrs: dict):
        """ Метод валидации передаваемых от пользователя данных """
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Пользователь или пароль неверный.')
        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    """ Сериализатор для профиля пользователя """
    class Meta:
        model = USER_MODEL
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class UpdatePasswordSerializer(serializers.ModelSerializer):
    """ Сериализатор для обновления пароля пользователя """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = USER_MODEL
        read_only_fields = ("id",)
        fields = ("user", "old_password", "new_password")

    def validate(self, attrs):
        """ Метод сверки текущего и вводимого паролей """
        user = attrs['user']
        if not user.check_password(attrs['old_password']):
            raise ValidationError({"old_password": "неверный пароль"})
        return attrs

    def update(self, instance: USER_MODEL, validated_data):
        """ Метод для обновления старого на новый """
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для данных пользователя """
    class Meta:
        model = USER_MODEL
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]
