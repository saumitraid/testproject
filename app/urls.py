from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Registration
    path(
        "register/",
        views.register,
        name="register"
    ),

    # Login
    path(
        "login/",
        views.user_login,
        name="login"
    ),

    # Logout
    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),
    path("verify-email/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    # Resend verification
    path(
        "resend-verification/",
        views.resend_verification,
        name="resend_verification"
    ),
]