# -*- coding: utf-8 -*-

from django import template

register = template.Library()

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

