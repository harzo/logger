from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': 'True'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'True'}))
