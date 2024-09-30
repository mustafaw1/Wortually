from django.urls import path
from .views import VerifyOTPView

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path("verify_otp/", VerifyOTPView.as_view(), name="verify_otp"),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    # path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
