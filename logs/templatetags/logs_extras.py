# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.simple_tag
def work_time_text(start_time, end_time, gap_time):
    time_diff = end_time - start_time
    worktime = time_diff.total_seconds()
    if gap_time:
        worktime = worktime - int(gap_time*3600)
    rest = worktime % 3600
    minutes = int(rest/60)
    hours = int(worktime/3600)

    return str(hours)+'h '+str(minutes)+'m'

@register.simple_tag
def seconds_to_time_text(seconds):
    if seconds:
        rest = seconds % 3600
        minutes = int(rest/60)
        hours = int(seconds/3600)

        return str(hours)+'h '+str(minutes)+'m'
    else:
        return '0h'

@register.simple_tag
def gap_time_to_text(gap_time):
    if gap_time:
        gap_time = int(gap_time * 60)
        minutes = gap_time % 60
        hours = int(gap_time/60)

        return str(hours)+'h '+str(minutes)+'m'
    else:
        return '0h 0m'

@register.assignment_tag
def concat_to_var(one, two):
    return str(one)+str(two)

@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.simple_tag
def int_to_weekday(daynb):
    daynb = str(daynb)
    return {
        '0': '---',
        '1': 'Poniedziałek',
        '2': 'Wtorek',
        '3': 'Środa',
        '4': 'Czwartek',
        '5': 'Piątek',
    }[daynb]

@register.simple_tag
def int_to_type(typenb):
    typenb = str(typenb)
    return {
        '1': 'Cykliczna',
        '2': 'Jednodniowa',
        '3': 'Okresowa',
    }[typenb]



