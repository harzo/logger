from django import forms


class LogForm(forms.Form):
    summary = forms.CharField(widget=forms.Textarea(attrs={'required': ''}))
    problems = forms.CharField(widget=forms.Textarea())

    hours = [['%02d' % i, '%02d' % i] for i in range(24)]
    minutes = [['%02d' % i, '%02d' % i] for i in range(60)]

    start_hour = forms.CharField(widget=forms.Select(choices=hours))
    start_minute = forms.CharField(widget=forms.Select(choices=minutes))
    end_hour = forms.CharField(widget=forms.Select(choices=hours))
    end_minute = forms.CharField(widget=forms.Select(choices=minutes))

    gaps = [['%.1f' % float(float(i)/2.0), '%.1f' % float(float(i)/2.0)] for i in range(20)]
    gap_time = forms.CharField(widget=forms.Select(choices=gaps))