# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
import datetime
from .models import Log
from django.contrib.auth.models import User, Group
from settings.models import Gap
from django.contrib.auth.decorators import login_required
from .forms import LogForm
from calendar import monthrange
from django.db.models import Q

@login_required
def index(request):
    latest_log = Log.objects.all()

    return render(request, 'logs/index.html', {
        'latest_log': latest_log,
    })

@login_required
def editlog(request, id_log=0):

    now = datetime.datetime.now()

    if id_log == 0:
        return HttpResponseRedirect('/summary')

    try:
        todays_log = Log.objects.get(
            pk=id_log,
            start_time__year=now.year,
            start_time__month=now.month,
            start_time__day=now.day,
            id_user=request.user
        )
    except Log.DoesNotExist:
        return HttpResponseRedirect('/summary')

    if not todays_log:
        return HttpResponseRedirect('/summary')

    if request.method == 'POST':
        form = LogForm(request.POST)

        day = now.strftime("%Y-%m-%d")

        if int(request.POST['start_hour']) > int(request.POST['end_hour']) \
            or (int(request.POST['start_hour']) == int(request.POST['end_hour']) and int(request.POST['start_minute']) >= int(request.POST['end_minute'])):

            return render(request, 'logs/logme.html', {'error': 'Błędny przedział czasowy. Spróbuj ponownie.', 'form': form, 'now': now})

        todays_log.summary = request.POST['summary']
        todays_log.problems = request.POST['problems']
        todays_log.start_time = day+' '+request.POST['start_hour']+':'+request.POST['start_minute']
        todays_log.end_time = day+' '+request.POST['end_hour']+':'+request.POST['end_minute']
        todays_log.gap_time = float(request.POST['gap_time'])
        todays_log.save()

        return HttpResponseRedirect('/summary')
    else:
        form = LogForm(initial={
            'start_hour': todays_log.start_time.strftime("%H"),
            'start_minute': todays_log.start_time.strftime("%M"),
            'end_hour': todays_log.end_time.strftime("%H"),
            'end_minute': todays_log.end_time.strftime("%M"),
            'summary': todays_log.summary,
            'problems': todays_log.problems,
            'gap_time': todays_log.gap_time
        })

    return render(request, 'logs/editlog.html', {'form': form, 'now': now, 'id_log': id_log})

@login_required
def logme(request):
    now = datetime.datetime.now()
    todays_log = Log.objects.filter(
        start_time__year=now.year,
        start_time__month=now.month,
        start_time__day=now.day,
        id_user=request.user
    )
    if todays_log:
        return HttpResponseRedirect('/profile')

    if request.method == 'POST':
        form = LogForm(request.POST)

        day = now.strftime("%Y-%m-%d")

        if int(request.POST['start_hour']) > int(request.POST['end_hour']) \
            or (int(request.POST['start_hour']) == int(request.POST['end_hour']) and int(request.POST['start_minute']) >= int(request.POST['end_minute'])):

            return render(request, 'logs/logme.html', {'error': 'Błędny przedział czasowy. Spróbuj ponownie.', 'form': form, 'now': now})

        l = Log(
                id_user = request.user,
                summary = request.POST['summary'],
                problems = request.POST['problems'],
                start_time = day+' '+request.POST['start_hour']+':'+request.POST['start_minute'],
                end_time = day+' '+request.POST['end_hour']+':'+request.POST['end_minute'],
                gap_time = float(request.POST['gap_time']),
                closed = True)

        todays_log = Log.objects.filter(
            start_time__year=now.year,
            start_time__month=now.month,
            start_time__day=now.day,
            id_user=request.user
        )
        if not todays_log:
            l.save()
        if l.id is None:
            return render(request, 'logs/logme.html', {'error': 'Błąd podczas dodawania. Spróbuj ponownie.', 'form': form, 'now': now})

        return HttpResponseRedirect('/profile')
    else:
        form = LogForm()

    return render(request, 'logs/logme.html', {'form': form, 'now': now})

@login_required
def reportmonth(request, month=0, year=0):

    employer = Group.objects.get(name='Employer')
    if not employer in request.user.groups.all() and not request.user.is_superuser:
        return HttpResponseRedirect('/profile/')

    now = datetime.datetime.now()

    if month == 0:
        month = now.month

    if year == 0:
        year = now.year

    logs = Log.objects.filter(
        start_time__month=month,
        start_time__year=year,
    ).order_by('-start_time')

    month_days = range(1, (monthrange(int(year), int(month)))[1]+1)

    gaps = Gap.objects.filter(
        Q(
        start_time__month=month,
        start_time__year=year
        ) |
        Q(
        end_time__month=month,
        end_time__year=year
        ) |
        Q(
        start_time__lte = datetime.datetime(int(year), int(month), 1),
        end_time__gte = datetime.datetime(int(year), int(month), month_days[-1])
        )
    ).order_by('-start_time')

    logs_dict = {}
    logs_time_dics = {}
    for i in month_days:
        logs_time_dics[i] = 0

    month_worktime = 0

    last_day = None
    last_user = None

    for log in logs:
        if log.start_time.day != last_day or log.id_user != last_user:
            time_diff = log.end_time - log.start_time
            gap_time = 0 if not log.gap_time else log.gap_time
            month_worktime = month_worktime + time_diff.total_seconds() - int(gap_time*3600)
            logs_time_dics[log.start_time.day] += time_diff.total_seconds() - int(gap_time*3600)

            if log.start_time.day not in logs_dict:
                logs_dict[log.start_time.day] = {}
            logs_dict[log.start_time.day][len(logs_dict[log.start_time.day])] = log

            last_day = log.start_time.day
            last_user = log.id_user

    for gap in gaps:
        if int(gap.type) == 1:
            time_diff = gap.end_time - gap.start_time
            days_diff = int(time_diff.total_seconds()/86400)

            if int(gap.start_time.month) == int(month):
                if days_diff+int(gap.start_time.day)-1 > month_days[-1]:
                    days_diff = month_days[-1]-int(gap.start_time.day)+1

                for dd in range(int(gap.start_time.day), int(gap.start_time.day)+days_diff):
                    weekday = datetime.datetime(int(year), int(month), dd)
                    weekday = int(weekday.strftime("%w"))

                    if weekday == 0:
                        weekday = 7
                    if gap.week_day == weekday:
                        if dd not in logs_dict:
                            logs_dict[dd] = {}
                        logs_dict[dd][len(logs_dict[dd])] = gap

            elif int(gap.start_time.month) < int(month):
                if int(gap.end_time.month) > int(month):
                    days_diff = month_days[-1]
                else:
                    days_diff = int(gap.end_time.day)

                for dd in range(1, days_diff+1):
                    weekday = datetime.datetime(int(year), int(month), dd)
                    weekday = int(weekday.strftime("%w"))

                    if weekday == 0:
                        weekday = 7
                    if gap.week_day == weekday:
                        if dd not in logs_dict:
                            logs_dict[dd] = {}
                        logs_dict[dd][len(logs_dict[dd])] = gap

        elif int(gap.type) == 2:
            if gap.start_time.day not in logs_dict:
                logs_dict[gap.start_time.day] = {}
            logs_dict[gap.start_time.day][len(logs_dict[gap.start_time.day])] = gap

        else:
            time_diff = gap.end_time - gap.start_time
            days_diff = int(time_diff.total_seconds()/86400)

            if int(gap.start_time.month) == int(month):
                if days_diff+int(gap.start_time.day)-1 > month_days[-1]:
                    days_diff = month_days[-1]-int(gap.start_time.day)+1

                for dd in range(int(gap.start_time.day), int(gap.start_time.day)+days_diff):
                    if dd not in logs_dict:
                        logs_dict[dd] = {}
                    logs_dict[dd][len(logs_dict[dd])] = gap

            elif int(gap.start_time.month) < int(month):
                if int(gap.end_time.month) > int(month):
                    days_diff = month_days[-1]
                else:
                    days_diff = int(gap.end_time.day)

                for dd in range(1, days_diff+1):
                    if dd not in logs_dict:
                        logs_dict[dd] = {}
                    logs_dict[dd][len(logs_dict[dd])] = gap

    missing_reports = 0
    for i in month_days:
        if i not in logs_dict:
            if int(month) < now.month or (int(month) == now.month and i <= now.day):
                logs_dict[i] = 0
                missing_reports += 1
            else:
                logs_dict[i] = None

    return render(request, 'logs/reportmonth.html', {
        'logs_dict': logs_dict,
        'logs_time_dics': logs_time_dics,
        'missing_reports': missing_reports,
        'prev': datetime.datetime(int(year), int(month)-1, 1) if int(month) > 1 else datetime.datetime(int(year)-1, 12, 1),
        'chosen': datetime.datetime(int(year), int(month), int(now.strftime("%d"))),
        'current_day': str(now.day)+now.strftime("-%m-%Y"),
        'next': datetime.datetime(int(year), int(month)+1, 1) if int(month) < 12 else datetime.datetime(int(year)+1, 1, 1),
        'month_worktime': month_worktime,
        'current_month_fd_weekday': range(datetime.datetime(int(year), int(month), 1).weekday())
    })

@login_required
def choosereportuser(request):

    employer = Group.objects.get(name='Employer')
    if not employer in request.user.groups.all() and not request.user.is_superuser:
        return HttpResponseRedirect('/profile/')

    users = User.objects.filter(
        ~Q(pk=request.user.id)
    ).order_by('username')

    employees = []
    interns = []
    for user in users:
        intern = Group.objects.get(name='Intern')
        if intern in user.groups.all():
            interns.append(user)
        else:
            employees.append(user)

    now = datetime.datetime.now()

    return render(request, 'logs/choosereportuser.html', {
        'employees': employees,
        'interns': interns,
        'now': now
    })

@login_required
def reportuser(request, id_user, month=0, year=0):

    employer = Group.objects.get(name='Employer')
    if not employer in request.user.groups.all() and not request.user.is_superuser:
        return HttpResponseRedirect('/profile/')

    now = datetime.datetime.now()

    if month == 0:
        month = now.month

    if year == 0:
        year = now.year

    user = get_object_or_404(User, pk=int(id_user))

    logs = Log.objects.filter(
        start_time__month=month,
        start_time__year=year,
        id_user=user
    ).order_by('-start_time')

    month_days = range(1, (monthrange(int(year), int(month)))[1]+1)

    gaps = Gap.objects.filter(
        Q(
        start_time__month=month,
        start_time__year=year,
        id_user=user
        ) |
        Q(
        end_time__month=month,
        end_time__year=year,
        id_user=user
        ) |
        Q(
        start_time__lte = datetime.datetime(int(year), int(month), 1),
        end_time__gte = datetime.datetime(int(year), int(month), month_days[-1]),
        id_user=user
        )
    ).order_by('-start_time')

    logs_dict = {}
    month_worktime = 0
    last_day = None
    for log in logs:
        if log.start_time.day != last_day:
            time_diff = log.end_time - log.start_time
            gap_time = 0 if not log.gap_time else log.gap_time
            month_worktime = month_worktime + time_diff.total_seconds() - int(gap_time*3600)
            logs_dict[log.start_time.day] = log
            last_day = log.start_time.day

    rest = month_worktime % 3600
    month_minutes = int(rest/60)
    month_hours = int(month_worktime/3600)

    for gap in gaps:
        if int(gap.type) == 1:
            time_diff = gap.end_time - gap.start_time
            days_diff = int(time_diff.total_seconds()/86400)

            if int(gap.start_time.month) == int(month):
                if days_diff+int(gap.start_time.day)-1 > month_days[-1]:
                    days_diff = month_days[-1]-int(gap.start_time.day)+1

                for dd in range(int(gap.start_time.day), int(gap.start_time.day)+days_diff):
                    weekday = datetime.datetime(int(year), int(month), dd)
                    weekday = int(weekday.strftime("%w"))

                    if weekday == 0:
                        weekday = 7
                    if gap.week_day == weekday:
                        if dd not in logs_dict:
                            logs_dict[dd] = gap

            elif int(gap.start_time.month) < int(month):
                if int(gap.end_time.month) > int(month):
                    days_diff = month_days[-1]
                else:
                    days_diff = int(gap.end_time.day)

                for dd in range(1, days_diff+1):
                    weekday = datetime.datetime(int(year), int(month), dd)
                    weekday = int(weekday.strftime("%w"))

                    if weekday == 0:
                        weekday = 7
                    if gap.week_day == weekday:
                        if dd not in logs_dict:
                            logs_dict[dd] = gap

        elif int(gap.type) == 2:
            logs_dict[gap.start_time.day] = gap

        else:
            time_diff = gap.end_time - gap.start_time
            days_diff = int(time_diff.total_seconds()/86400)

            if int(gap.start_time.month) == int(month):
                if days_diff+int(gap.start_time.day)-1 > month_days[-1]:
                    days_diff = month_days[-1]-int(gap.start_time.day)+1

                for dd in range(int(gap.start_time.day), int(gap.start_time.day)+days_diff):
                    if dd not in logs_dict:
                        logs_dict[dd] = gap

            elif int(gap.start_time.month) < int(month):
                if int(gap.end_time.month) > int(month):
                    days_diff = month_days[-1]
                else:
                    days_diff = int(gap.end_time.day)

                for dd in range(1, days_diff+1):
                    logs_dict[dd] = gap

    missing_reports = 0
    for i in month_days:
        if i not in logs_dict:
            weekday = datetime.datetime(int(year), int(month), i)
            weekday = int(weekday.strftime("%w"))
            if (int(month) < now.month or (int(month) == now.month and i <= now.day)) and not weekday == 0 and not weekday == 6:
                logs_dict[i] = 0
                missing_reports += 1
            else:
                logs_dict[i] = None

    return render(request, 'logs/reportuser.html', {
        'user': user,
        'logs_dict': logs_dict,
        'missing_reports': missing_reports,
        'prev': datetime.datetime(int(year), int(month)-1, 1) if int(month) > 1 else datetime.datetime(int(year)-1, 12, 1),
        'chosen': datetime.datetime(int(year), int(month), 1),
        'current_day': now.strftime("%d-%m-%Y"),
        'next': datetime.datetime(int(year), int(month)+1, 1) if int(month) < 12 else datetime.datetime(int(year)+1, 1, 1),
        'current_month_worktime': str(month_hours)+'h '+str(month_minutes)+'m',
        'current_month_fd_weekday': range(datetime.datetime(int(year), int(month), 1).weekday())
    })

@login_required
def summary(request, month=0, year=0):

    now = datetime.datetime.now()

    if month == 0:
        month = now.month

    if year == 0:
        year = now.year

    logs = Log.objects.filter(
        start_time__month=month,
        start_time__year=year,
        id_user=request.user
    ).order_by('-start_time')

    month_days = range(1, (monthrange(int(year), int(month)))[1]+1)

    gaps = Gap.objects.filter(
        Q(
        start_time__month=month,
        start_time__year=year,
        id_user=request.user
        ) |
        Q(
        end_time__month=month,
        end_time__year=year,
        id_user=request.user
        ) |
        Q(
        start_time__lte = datetime.datetime(int(year), int(month), 1),
        end_time__gte = datetime.datetime(int(year), int(month), month_days[-1]),
        id_user=request.user
        )
    ).order_by('-start_time')

    logs_dict = {}
    month_worktime = 0
    last_day = None
    for log in logs:
        if log.start_time.day != last_day:
            time_diff = log.end_time - log.start_time
            gap_time = 0 if not log.gap_time else log.gap_time
            month_worktime = month_worktime + time_diff.total_seconds() - int(gap_time*3600)
            logs_dict[log.start_time.day] = log
            last_day = log.start_time.day

    rest = month_worktime % 3600
    month_minutes = int(rest/60)
    month_hours = int(month_worktime/3600)

    for gap in gaps:
        if int(gap.type) == 1:
            time_diff = gap.end_time - gap.start_time
            days_diff = int(time_diff.total_seconds()/86400)

            if int(gap.start_time.month) == int(month):
                if days_diff+int(gap.start_time.day)-1 > month_days[-1]:
                    days_diff = month_days[-1]-int(gap.start_time.day)+1

                for dd in range(int(gap.start_time.day), int(gap.start_time.day)+days_diff):
                    weekday = datetime.datetime(int(year), int(month), dd)
                    weekday = int(weekday.strftime("%w"))

                    if weekday == 0:
                        weekday = 7
                    if gap.week_day == weekday:
                        logs_dict[dd] = gap

            elif int(gap.start_time.month) < int(month):
                if int(gap.end_time.month) > int(month):
                    days_diff = month_days[-1]
                else:
                    days_diff = int(gap.end_time.day)

                for dd in range(1, days_diff+1):
                    weekday = datetime.datetime(int(year), int(month), dd)
                    weekday = int(weekday.strftime("%w"))

                    if weekday == 0:
                        weekday = 7
                    if gap.week_day == weekday:
                        logs_dict[dd] = gap

        elif int(gap.type) == 2:
            logs_dict[gap.start_time.day] = gap

        else:
            time_diff = gap.end_time - gap.start_time
            days_diff = int(time_diff.total_seconds()/86400)

            if int(gap.start_time.month) == int(month):
                if days_diff+int(gap.start_time.day)-1 > month_days[-1]:
                    days_diff = month_days[-1]-int(gap.start_time.day)+1

                for dd in range(int(gap.start_time.day), int(gap.start_time.day)+days_diff):
                    logs_dict[dd] = gap

            elif int(gap.start_time.month) < int(month):
                if int(gap.end_time.month) > int(month):
                    days_diff = month_days[-1]
                else:
                    days_diff = int(gap.end_time.day)

                for dd in range(1, days_diff+1):
                    logs_dict[dd] = gap

    missing_reports = 0
    for i in month_days:
        if i not in logs_dict:
            weekday = datetime.datetime(int(year), int(month), i)
            weekday = int(weekday.strftime("%w"))
            if (int(month) < now.month or (int(month) == now.month and i <= now.day)) and not weekday == 0 and not weekday == 6:
                logs_dict[i] = 0
                missing_reports += 1
            else:
                logs_dict[i] = None

    return render(request, 'logs/summary.html', {
        'logs_dict': logs_dict,
        'missing_reports': missing_reports,
        'prev': datetime.datetime(int(year), int(month)-1, 1) if int(month) > 1 else datetime.datetime(int(year)-1, 12, 1),
        'chosen': datetime.datetime(int(year), int(month), 1),
        'current_day': str(now.day)+now.strftime("-%m-%Y"),
        'next': datetime.datetime(int(year), int(month)+1, 1) if int(month) < 12 else datetime.datetime(int(year)+1, 1, 1),
        'current_month_worktime': str(month_hours)+'h '+str(month_minutes)+'m',
        'current_month_fd_weekday': range(datetime.datetime(int(year), int(month), 1).weekday())
    })
