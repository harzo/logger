# -*- coding: utf-8 -*-

from django import forms
from django.forms import extras
import datetime


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'True'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'True'}))
    password_conf = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'True'}))


class GapAddForm(forms.Form):
    types = [
        ['1', 'Cykliczna'],
        ['2', 'Jednoniowa'],
        ['3', 'Okresowa']
    ]
    type = forms.CharField(widget=forms.Select(choices=types))

    days = [
        ['1', 'Poniedziałek'],
        ['2', 'Wtorek'],
        ['3', 'Środa'],
        ['4', 'Czwartek'],
        ['5', 'Piątek']
    ]
    week_day = forms.CharField(widget=forms.Select(choices=days))

    start_date = forms.DateField(initial=datetime.date.today, input_formats='%Y-%m-%d', widget=extras.SelectDateWidget())
    end_date = forms.DateField(initial=datetime.datetime(int(datetime.datetime.now().strftime("%Y"))+9, 12, 31), input_formats='%Y-%m-%d', widget=extras.SelectDateWidget())
