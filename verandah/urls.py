from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	url(r'^$', 'core.views.homepage', name = 'home'),
    url(r'^calendar/', include('cal.urls')),
        
    url(r'^typewriter$', 'typewriter.views.dashboard', name = 'typewriter'),
    url(r'^typewriter/document/(?P<document_name>[a-zA-z0-9_]*)$', 'typewriter.views.document', name = 'typewriter_document'),

	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),


	url(r'^user/edit$', 'core.views.homepage', name = 'user-edit'),
	url(r'^login$', 'django.contrib.auth.views.login', name = 'login'),
	url(r'^logout$', 'django.contrib.auth.views.logout', name = 'logout'),

)

if settings.CONFIG == 'dev':
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	)	