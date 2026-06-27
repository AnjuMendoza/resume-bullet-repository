from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import EmailLoginForm, SignupForm
from .models import Bullet


def bullet_list(request):
    bullets = Bullet.objects.all()
    return render(request, 'bullet_list.html', {'bullets': bullets})


def account_view(request):
    if request.user.is_authenticated:
        return redirect('bullet_list')

    login_form = EmailLoginForm(prefix='login')
    signup_form = SignupForm(prefix='signup')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            login_form = EmailLoginForm(request, request.POST, prefix='login')
            if login_form.is_valid():
                login(request, login_form.user)
                messages.success(request, 'Welcome back!')
                return redirect('bullet_list')
            messages.error(request, 'Please check your login details.')

        elif action == 'signup':
            signup_form = SignupForm(request.POST, prefix='signup')
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, 'Your account is ready. Welcome!')
                return redirect('bullet_list')
            messages.error(request, 'Please fix the signup form errors.')

    return render(
        request,
        'account.html',
        {
            'login_form': login_form,
            'signup_form': signup_form,
        },
    )


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
    return redirect('bullet_list')
