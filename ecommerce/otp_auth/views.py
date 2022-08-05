from datetime import datetime
import pyotp
from .models import Profile
import base64
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView
from django.contrib import messages


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        check_user = User.objects.filter(email=email).first()

        if check_user:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'register.html', context)

        user, created = User.objects.get_or_create(email=email)
        user.save()
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(email).encode())
        otp = pyotp.HOTP(key)
        abc = otp.at(0)
        print(abc)
        profile = Profile(user=user, email=email, otp=abc)
        profile.save()
        request.session['email'] = email
        return redirect('otp')
    return render(request, 'register.html')


def otp(request):
    email = request.session['email']
    context = {'email': email}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(email=email).first()

        if otp == profile.otp:
            return redirect(reverse('home'))
        else:
            print('Wrong')
            context = {'message': 'Wrong OTP', 'class': 'danger', 'email': email}
            return render(request, 'otp.html', context)

    return render(request, 'otp.html', context)


def login_otp(request):
    email = request.session['email']
    context = {'email': email}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(email=email).first()

        if otp == profile.otp:
            user = User.objects.get(id=profile.user.id)
            login(request, user)
            return redirect('home')
        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'email': email}
            return render(request, 'otp.html', context)

    return render(request, 'login.html', context)


def resend_otp(request):
    email = request.session['email']
    profile = Profile.objects.filter(email=email).first()
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(email).encode())
    otp = pyotp.HOTP(key)
    resend_count = profile.resend_count + 1
    abc = otp.at(resend_count)
    profile.otp = abc
    profile.resend_count = resend_count
    print(abc)
    profile.save()
    return redirect('otp')


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

