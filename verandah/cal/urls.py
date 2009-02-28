from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
    url(r'$', 'cal.views.dashboard', name = 'calendar'),
    url(r'month/(?P<year>\d{4})/(?P<month>\d{2})$', 'cal.views.dashboard', name = 'calendar_month'),
)