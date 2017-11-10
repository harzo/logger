# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import PasswordChangeForm, GapAddForm
from accounts.views import passch_user
from .models import Gap
import datetime
from calendar import monthrange
from django.http import HttpResponseRedirect

@login_required
def settings_user(request):
    form = PasswordChangeForm()
    form2 = GapAddForm()

    now = datetime.datetime.now()
    """st = datetime.date(now.year, now.month, now.day)
    gaps = Gap.objects.filter(
        start_time__gte=st,
        id_user=request.user
    )"""
    gaps = Gap.objects.filter(
        id_user=request.user
    )

    if request.method == 'POST':
        if request.POST['action'] == 'passch':
            form = PasswordChangeForm(request.POST)
            if passch_user(request):
                user = authenticate(username=request.user.username, password=request.POST['new_password'].strip())
                login(request, user)
                return render(request, 'settings/settings.html', {'form': form, 'form2': form2, 'success': 'Hasło zostało zmienione.', 'gaps': gaps, 'now': now})
            else:
                return render(request, 'settings/settings.html', {'form': form, 'form2': form2, 'error': 'Podane dane są niepoprawne. Spróbuj ponownie.', 'gaps': gaps, 'now': now})
        elif request.POST['action'] == 'gapadd':
            form2 = GapAddForm(request.POST)

            sd = int(request.POST['start_date_day'])
            month_days = monthrange(int(request.POST['start_date_year']), int(request.POST['start_date_month']))[1]
            if sd > month_days:
                sd = str(month_days)

            ed = int(request.POST['end_date_day'])
            month_days = monthrange(int(request.POST['end_date_year']), int(request.POST['end_date_month']))[1]
            if ed > month_days:
                ed = str(month_days)

            st = datetime.date(int(request.POST['start_date_year']), int(request.POST['start_date_month']), int(sd))
            et = datetime.date(int(request.POST['end_date_year']), int(request.POST['end_date_month']), int(ed))
            today = datetime.date.today()

            if st > et:
                return render(request, 'settings/settings.html', {'form': form, 'form2': form2, 'error2': 'Błędny okres. Spróbuj ponownie.', 'gaps': gaps, 'now': now})

            if st < today:
                if int(request.POST['type']) == 2:
                    return render(request, 'settings/settings.html', {'form': form, 'form2': form2, 'error2': 'Podana data odnosi się do przeszłości. Spróbuj ponownie.', 'gaps': gaps, 'now': now})
                return render(request, 'settings/settings.html', {'form': form, 'form2': form2, 'error2': 'Podany okres odnosi się do przeszłości. Spróbuj ponownie.', 'gaps': gaps, 'now': now})

            g = Gap(
                    id_user=request.user,
                    type=request.POST['type'],
                    week_day=request.POST['week_day'] if int(request.POST['type']) == 1 else 0,
                    start_time=request.POST['start_date_year']+'-'+request.POST['start_date_month']+'-'+str(sd)+' 00:00:00',
                    end_time=request.POST['start_date_year']+'-'+request.POST['start_date_month']+'-'+str(sd)+' 00:00:00' if int(request.POST['type']) == 2 else request.POST['end_date_year']+'-'+request.POST['end_date_month']+'-'+str(ed)+' 00:00:00',
                    )
            g.save()
            if g.id is None:
                return render(request, 'settings/settings.html', {'form': form, 'form2': form2, 'error2': 'Błąd podczas dodawania. Spróbuj ponownie.', 'gaps': gaps, 'now': now})

            return render(request, 'settings/settings.html', {'form': form, 'form2': form2, 'success2': 'Przerwa została dodana', 'gaps': gaps, 'now': now})

    return render(request, 'settings/settings.html', {'form': form, 'form2': form2, 'gaps': gaps, 'now': now})

@login_required
def delgap(request, id_gap=0):
    try:
        gap = Gap.objects.get(
            pk=id_gap,
            id_user=request.user
        )

        gap.delete()
        return HttpResponseRedirect('/settings')

    except Gap.DoesNotExist:
        return HttpResponseRedirect('/settings')