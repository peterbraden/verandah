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

def dashboard(request, year = None, month = None):
	date = datetime.datetime.now()
 
	context = {
		'month' : cal.models.Month(year and int(year) or date.year, month and int(month) or date.month),
		'calendars' :cal.models.Calendar.objects.all(),
	} 
	return _render(request, 'calendar_dashboard.html', context)