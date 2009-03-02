import datetime

from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

import cal.models
from cal.forms import CalendarForm, EventForm


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
		'agenda' : cal.models.Agenda(request.user),
	} 
	context['events'] = list(set(context['agenda']))
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
	
@login_required
def event(request, event_id = None):
	if request.method == 'GET':
		if event_id:
			form = EventForm(instance = get_object_or_404(cal.models.Event, id = event_id))
		else:
			form = EventForm()
			
	if request.method == 'POST':
		instance = None
		if event_id:
			instance = EventForm(instance = get_object_or_404(Event, id = event_id))	
		form = EventForm(request.POST, instance = instance)
	
	context = {
		'form' : form	
	}

	return _render(request, 'cal/templates/edit-event.html', context)		
	