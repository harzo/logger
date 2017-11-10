from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
    id_user = models.ForeignKey(User)
    summary = models.TextField()
    problems = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    gap_time = models.FloatField(null=True, blank=True)
    closed = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True, null=True)
    date_mod = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return u'{s}'.format(s=self.summary)
