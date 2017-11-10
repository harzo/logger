from django.db import models
from django.contrib.auth.models import User

class Gap(models.Model):
    id_user = models.ForeignKey(User)
    type = models.IntegerField()
    week_day = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date_add = models.DateTimeField(auto_now_add=True, null=True)
    date_mod = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.type)+' '+str(self.week_day)+' '+str(self.start_time)+' '+str(self.end_time)