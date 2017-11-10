# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm
from logs.models import Log
import datetime


@login_required
def profile_user(request):
    user_groups = request.user.groups.all()

    now = datetime.datetime.now()
    todays_log = Log.objects.filter(
        start_time__year=now.year,
        start_time__month=now.month,
        start_time__day=now.day,
        end_time__year=now.year,
        end_time__month=now.month,
        end_time__day=now.day,
        id_user=request.user
    )

    return render(request, 'accounts/profile.html', {'user_groups': user_groups, 'todays_log': todays_log})


@login_required
def passch_user(request):
    if request.method == 'POST':
        if request.POST['old_password'] and request.POST['new_password'] and request.POST['password_conf']:
            u = User.objects.get(id=request.user.id)
            if u.check_password(request.POST['old_password'].strip()):
                if request.POST['new_password'] == request.POST['password_conf']:
                    u.set_password(request.POST['new_password'].strip())
                    u.save()
                    return True
    return False

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/profile/')
            else:
                return render(request, 'accounts/login.html', {'error': 'Konto nieaktywne. Skontaktuj się z administratorem.', 'form': form})
        else:
            return render(request, 'accounts/login.html', {'error': 'Błędne dane logowania. Spróbuj ponownie.', 'form': form})
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/profile/')
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')