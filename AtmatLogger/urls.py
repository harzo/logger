from django.conf.urls import include, url
from django.contrib import admin
from django.template.response import TemplateResponse

urlpatterns = [
    url(r'^$', 'accounts.views.login_user'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'accounts.views.login_user'),
    url(r'^logout/', 'accounts.views.logout_user'),
    url(r'^profile/', include('accounts.urls', namespace='accounts')),
    url(r'^summary/', include('logs.urls', namespace='logs')),
    url(r'^logme/', 'logs.views.logme'),
    url(r'^report/', include('logs.urls', namespace='logs')),
    url(r'^editlog/$', 'logs.views.editlog'),
    url(r'^editlog/(?P<id_log>[0-9]+)/', 'logs.views.editlog'),
    url(r'^delgap/$', 'settings.views.delgap'),
    url(r'^delgap/(?P<id_gap>[0-9]+)/', 'settings.views.delgap'),
    url(r'^settings/', 'settings.views.settings_user'),
]
