from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("helath-check", views.healthCheck),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
