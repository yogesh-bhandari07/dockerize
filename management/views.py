from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from management.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.http import HttpResponseRedirect
from .response_handler import *
import logging

logger = logging.getLogger(__name__)


def healthCheck():
    pass


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# auth


class UserRegistrationView(APIView):

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # token = get_tokens_for_user(user)

        a = SendEmailVerifyLinkSerializer(data={"email": request.data["email"]})
        a.is_valid(raise_exception=True)

        return custom_response(
            message="Account Verification link has been sent to your email",
            status=status.HTTP_201_CREATED,
        )


class VerifyUserEmailView(APIView):

    def get(self, request, uid, token, format=None):
        serializer = VerifyEmailSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)

        return HttpResponseRedirect(redirect_to=os.getenv("WEB_URL") + "login")


class UserLoginView(APIView):

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_verified:
                token = get_tokens_for_user(user)
                return custom_response(
                    data={
                        "token": token,
                        "user": {"name": user.name, "email": user.email},
                    },
                    message="Login Success",
                    status=status.HTTP_200_OK,
                )
            else:
                return custom_response(
                    success=False,
                    message="Please verify your account",
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return custom_response(
                success=False,
                message="Email or Password is not valid",
                status=status.HTTP_404_NOT_FOUND,
            )


class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return custom_response(data=serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return custom_response(
            message="Password Changed Successfully", status=status.HTTP_200_OK
        )


class SendPasswordResetEmailView(APIView):

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return custom_response(
            message="Password Reset link sent. Please check your Email",
            status=status.HTTP_200_OK,
        )


class UserPasswordResetView(APIView):

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return custom_response(
            message="Password Reset Successfully", status=status.HTTP_200_OK
        )


class UserView(APIView):
    def get(self, request, pk=None, format=None):
        logger.info(f"Users")
        id = pk
        if id is not None:
            module = User.objects.get(id=id)
            serializer = UserSerializer(module)
            return custom_response(data=serializer.data)
        modules = User.objects.filter(is_admin=False)
        serializer = UserSerializer(modules, many=True)
        return custom_response(
            message="Data Fetched", data=serializer.data, status=status.HTTP_200_OK
        )

    def put(self, request, pk, format=None):
        id = pk
        module = User.objects.get(id=id)
        serializer = UserSerializer(module, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custom_response(
            message="Data updated", data=serializer.data, status=status.HTTP_200_OK
        )

    def patch(self, request, pk, format=None):
        id = pk
        module = User.objects.get(id=id)
        serializer = UserSerializer(module, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custom_response(
            message="Data updated partially",
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk, format=None):
        id = pk
        module = User.objects.get(id=id)
        module.delete()
        return custom_response(
            message="Data has been deleted", status=status.HTTP_200_OK
        )
