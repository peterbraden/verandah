from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('cal.views',
    url(r'^$', 'dashboard', name = 'calendar'),
    
    url(r'^year/(?P<year>\d{4})$', 'dashboard', name = 'calendar_year'),
    url(r'^month/(?P<year>\d{4})/(?P<month>\d{2})$', 'dashboard', name = 'calendar_month'),
    url(r'^week/(?P<year>\d{4})/(?P<month>\d{2})/(?P<date>\d{1})$', 'dashboard', name = 'calendar_week'),
	url(r'^date/(?P<year>\d{4})/(?P<month>\d{2})/(?P<date>\d{2})$', 'dashboard', name = 'calendar_day'),
	
	
	url(r'^event$', 'event', name = 'calendar-event-add'),
	url(r'^event/(?P<event_id>.*)$', 'event', name = 'calendar-event'),
	
	url(r'^sync/(?P<calendar>.*)$', 'sync', name = "sync"),
	url(r'^add$', 'add_calendar', name = "calendar-add"),
	
)