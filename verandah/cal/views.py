import datetime

from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

import cal.models
from cal.forms import CalendarForm


def _render(request, template, context = {}):
	"""
	Render the template with the appropriate context
	"""
	return HttpResponse(get_template(template).render(RequestContext(request, context)))

@login_required
def dashboard(request, year = None, month = None):
	
	date = datetime.datetime.now()
 
	context = {
		'month' : cal.models.Month(year and int(year) or date.year, month and int(month) or date.month, request.user),
		'calendars' : cal.models.Calendar.objects.filter(owner = request.user),
		'agenda' : cal.models.Event.objects.filter(calendar__owner = request.user, start__gt = date).order_by('start')[:10],
	} 
	return _render(request, 'cal/templates/calendar_dashboard.html', context)


@login_required
def sync(request, calendar):
	calendar = get_object_or_404(cal.models.Calendar, id = calendar)	
	cal.models.parse_iCal(calendar.urls, request.user, calendar)
	return HttpResponseRedirect(reverse('calendar'))

@login_required	
def add_calendar(request):
	if request.method == 'POST':
		form = CalendarForm(request.POST)
		if form.is_valid():
			c = form.save(commit = False)
			c.owner = request.user
			c.save()
			
			if c.urls:
				cal.models.parse_iCal(c.urls, request.user, c)
			
			return HttpResponseRedirect(reverse('calendar'))
	else:
		form = CalendarForm()

	context = {
		'form' : form	
	}

	return _render(request, 'cal/templates/edit.html', context)	