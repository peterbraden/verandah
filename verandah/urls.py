from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'cal.views.dashboard'),
)
