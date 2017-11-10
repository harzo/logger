from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.summary, name='summary'),
    url(r'^(?P<month>[0-9]+)/$', views.summary, name='month'),
    url(r'^(?P<month>[0-9]+),(?P<year>[0-9]+)/$', views.summary, name='month_year'),
    url(r'^month/$', views.reportmonth, name='reportmonth'),
    url(r'^month/(?P<month>[0-9]+)/$', views.reportmonth, name='reportmonth'),
    url(r'^month/(?P<month>[0-9]+),(?P<year>[0-9]+)/$', views.reportmonth, name='reportmonth'),
    url(r'^user/$', views.choosereportuser, name='reportuser'),
    url(r'^user/(?P<id_user>[0-9]+),(?P<month>[0-9]+)/$', views.reportuser, name='reportuser'),
    url(r'^user/(?P<id_user>[0-9]+),(?P<month>[0-9]+),(?P<year>[0-9]+)/$', views.reportuser, name='reportuser'),
]