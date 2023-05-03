from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_staff",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def validate(self, attrs):
        validator = super().validate(attrs)
        username = attrs.get("username")
        password = attrs.get("password")
        if len(username) < 8:
            raise serializers.ValidationError(
                {"username": "Username must be longer than or equal to 8 characters."},
            )
        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be longer than or equal to 8 characters."},
            )
        return validator

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        return user
