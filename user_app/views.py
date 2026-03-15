from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate,
    get_user_model
)
from django.db import IntegrityError

from .models import User

# Create your views here.
def base(request):

    return render(request, 'base.html')


def register(request):

    if request.method == 'GET':

        return render(request, 'user_app/register.html')

    elif request.method == 'POST':

        form = request.POST

        username = form.get('username')
        password = form.get('password')
        password_confirm = form.get('password_confirm')
        first_name = form.get('first-name')
        last_name = form.get('last-name')
        email = form.get('email')

        if password != password_confirm:
            return render(request, 'user_app/register.html', {'error': 'Passwords do not match.'})

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
        except IntegrityError:
            return render(request, 'user_app/register.html', {'error': 'Username already taken. Please choose another.'})

        django_login(request, user)

        return redirect(reverse('user_app:profile', kwargs={'username': user.username}))

# --------------------------------------------------------

def login(request):

    if request.method == 'GET':

        return render(request, 'user_app/login.html')

    elif request.method == 'POST':

        form = request.POST

        username = form.get('username')
        password = form.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            return redirect(reverse('user_app:profile', kwargs={'username': user.username}))

        return render(request, 'user_app/login.html', {'error': 'Invalid username or password.'})


# --------------------------------------------------------
@login_required
def profile(request, username):

    if request.method == 'GET':

        user = get_object_or_404(get_user_model(), username=username)

        context = {
            'user': user,
            'username': user.username,
        }

        return render(request, 'user_app/mem-dashboard.html', context)


# --------------------------------------------------------

def logout(request):

    django_logout(request)

    return redirect('user_app:base')
