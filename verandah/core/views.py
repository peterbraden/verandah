from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, Http404, HttpResponseRedirect

from datetime import datetime

import cal.models

def homepage(request):

	context = {
		'month' : cal.models.Month(datetime.today().year, datetime.today().month) 
	}
	
	return HttpResponse(get_template('home.html').render(RequestContext(request, context)))