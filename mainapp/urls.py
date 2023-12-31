import knox.views
from .views import RegisterAPI, LoginAPI, ChangePasswordView
from django.urls import path, include

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name="login"),
    path("api/logout/", knox.views.LogoutView.as_view(), name="logout"),
    path("api/logoutall/", knox.views.LogoutAllView.as_view(), name="logoutall"),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path("api/password_reset/", include("django_rest_passwordreset.urls"), name="password_reset"),
]

