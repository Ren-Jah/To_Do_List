from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.contrib.auth.hashers import make_password

USER_MODEL = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def create(self, validated_data) -> USER_MODEL:
        password = validated_data.get('password')
        password_repeat = validated_data.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError('Пароли не совпадают.')

        try:
            password_validation.validate_password(password)
        except Exception as e:
            raise serializers.ValidationError(e)

        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = USER_MODEL
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = USER_MODEL
        fields = ['username', 'password']

    def validate(self, attrs: dict):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Пользователь или пароль неверный.')
        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = USER_MODEL
        read_only_fields = ("id",)
        fields = ("old_password", "new_password")

    def validate(self, attrs):
        user = attrs['user']
        if not user.check_password(attrs['old_password']):
            raise ValidationError({"old_password": "неверный пароль"})
        return attrs

    def update(self, instance: USER_MODEL, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance
