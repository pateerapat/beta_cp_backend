from django.contrib.auth import login

from rest_framework import (
    generics,
    permissions,
)
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from knox.settings import CONSTANTS

from .serializers import (
    UserSerializer,
    RegisterSerializer,
)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data = request.data,
        )
        is_valid = serializer.is_valid()
        if is_valid:
            user = serializer.save()
            return Response({
                "user": UserSerializer(
                    user,
                    context = self.get_serializer_context(),
                ).data,
                "token": AuthToken.objects.create(user)[1],
            })

        errors = []
        for field_name, error_msg in serializer.errors.items():
            errors.append({
                "field_name": field_name,
                "error_msg": error_msg,
            })
        return Response({
            "errors": errors,
        })


class LoginAPI(KnoxLoginView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(
            data = request.data,
        )
        is_valid = serializer.is_valid()
        if is_valid:
            user = serializer.validated_data["user"]
            login(request, user)
            return super(LoginAPI, self).post(
                request,
                format = None,
            )

        errors = []
        for field_name, error_msg in serializer.errors.items():
            errors.append({
                "field_name": field_name,
                "error_msg": error_msg,
            })
        return Response({
            "errors": errors,
        })


class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        knox_token = AuthToken.objects.filter(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH]).first()
        if knox_token:
            return Response({
                "username": knox_token.user.username,
            })
        return Response({
            "errors": "Your session has been expired, Please login again."
        })
        # serializer = self.get_serializer(
        #     data = request.data,
        # )
        # is_valid = serializer.is_valid()
        # if is_valid:
        #     user = serializer.save()
        #     return Response({
        #         "user": UserSerializer(
        #             user,
        #             context = self.get_serializer_context(),
        #         ).data,
        #         "token": AuthToken.objects.create(user)[1],
        #     })

        # errors = []
        # for field_name, error_msg in serializer.errors.items():
        #     errors.append({
        #         "field_name": field_name,
        #         "error_msg": error_msg,
        #     })
        # return Response({
        #     "errors": errors,
        # })
