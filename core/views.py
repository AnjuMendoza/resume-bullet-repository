from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import EmailLoginForm, SignupForm
from .models import Bullet


def bullet_list(request):
    bullets = Bullet.objects.all()
    return render(request, 'bullet_list.html', {'bullets': bullets})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('bullet_list')

    form = EmailLoginForm(request, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.user)
            messages.success(request, 'Welcome back!')
            return redirect('bullet_list')
        messages.error(request, 'Please check your login details.')

    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('bullet_list')

    form = SignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account is ready. Welcome!')
            return redirect('bullet_list')
        messages.error(request, 'Please fix the signup form errors.')

    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
    return redirect('bullet_list')
