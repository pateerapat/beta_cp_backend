from rest_framework import serializers
from beta_user.models import BetaUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetaUser
        fields = [
            "id",
            "email",
            "username",
            "password",
            "is_staff",
            "is_active",
            "is_superuser",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetaUser
        fields = [
            "id",
            "username",
            "email",
            "password",
            "is_superuser",
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
        user = BetaUser.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        if validated_data["is_superuser"] == True:
            user.is_active = True
            user.is_superuser = True
            user.is_staff = True
            user.save()
        return user
