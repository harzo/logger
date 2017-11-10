from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.profile_user, name='profile_user'),
]