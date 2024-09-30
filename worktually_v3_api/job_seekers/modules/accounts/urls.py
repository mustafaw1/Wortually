from django.urls import path
from job_seekers.modules.accounts.views import *

urlpatterns = [
    path("jobseeker/register/", RegisterView.as_view(), name="register"),
    path("jobseeker/login", LoginView.as_view(), name="login"),
    path("jobseeker/logout/", LogoutView.as_view(), name="logout"),
    path(
        "jobseeker/forget-password/",
        ForgetPasswordView.as_view(),
        name="forget_password",
    ),
    path("jobseeker/verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path(
        "jobseeker/reset-password/", ResetPasswordView.as_view(), name="reset_password"
    ),
]
