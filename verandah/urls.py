from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	url(r'^$', 'core.views.homepage'),
    url(r'^calendar$', 'cal.views.dashboard', name = 'calendar'),
    url(r'^calendar/month/(?P<year>\d{4})/(?P<month>\d{2})$', 'cal.views.dashboard', name = 'calendar_month'),
    url(r'^typewriter$', 'typewriter.views.dashboard', name = 'typewriter'),
)

if settings.CONFIG == 'dev':
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	)	