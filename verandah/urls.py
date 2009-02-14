from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	url(r'^$', 'core.views.homepage'),
    url(r'^calendar/$', 'cal.views.dashboard'),
)

if settings.CONFIG == 'dev':
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	)	