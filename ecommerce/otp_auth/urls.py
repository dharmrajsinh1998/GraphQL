from django.urls import path
from .views import register, login_otp, otp, resend_otp, HomePageView
urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login_otp, name="login_with_otp"),
    path('otp', otp, name="otp"),
    path('resend-otp', resend_otp, name="resend_otp"),
    path('home', HomePageView.as_view(), name="home"),
]
