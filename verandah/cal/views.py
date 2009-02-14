import datetime

from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, Http404, HttpResponseRedirect


import cal.models


def _render(request, template, context = {}):
	"""
	Render the templat with the appropriate context
	"""
	return HttpResponse(get_template(template).render(RequestContext(request, context)))

def dashboard(request, date = None):
	date = date or datetime.datetime.now()
 
 	dates = [{'year': 2009, 'month' : i} for i in range(1,12)]
 
	context = {
		'months' : [cal.models.Month(date['year'], date['month']) for date in dates],
		'calendars' :cal.models.Calendar.objects.all(),
	} 
	return _render(request, 'calendar_dashboard.html', context)