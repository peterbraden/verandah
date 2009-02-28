from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	url(r'^$', 'core.views.homepage', name = 'home'),
    url(r'^calendar/', include('cal.urls')),
        
    url(r'^typewriter$', 'typewriter.views.dashboard', name = 'typewriter'),
    url(r'^typewriter/document/(?P<document_name>[a-zA-z0-9_]*)$', 'typewriter.views.document', name = 'typewriter_document'),

	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

)

if settings.CONFIG == 'dev':
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	)	