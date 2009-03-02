import datetime
import calendar
import urllib

from django.db import models
from django.contrib.auth.models import User

import settings
import icalendar 


def parse_iCal(url, owner, c = None):
	calendar = urllib.urlopen(url)
	cal = icalendar.Calendar.from_string(calendar.read())
	
	if not c:
		try:
			c = Calendar.objects.get(id = cal.decoded('X-WR-CALNAME'))
		except Calendar.DoesNotExist, e:	
			c = Calendar(
				id = cal.decoded('X-WR-CALNAME'),
				owner = owner,
				urls = url
			)
			c.save()
	
	for component in cal.walk():
		if component.name == 'VEVENT':
			
			def dat(param):
				"""
				Due to mysql crappery we discard timezone info. 
				"""
				if isinstance(component.decoded(param), datetime.datetime):
					return component.decoded(param).replace(tzinfo = None)
				return  component.decoded(param)
			
			kwargs = {
				'id' : component.decoded('uid'),
				'summary' : component.decoded('summary'),
				'cls' : component.decoded('class'),
				'description' : component.decoded('description'),
				'location' : component.decoded('location'),
				'status' : component.decoded('status'),
				'transp' : component.decoded('transp'),
				'sequence' : component.decoded('sequence'),
				'start' : dat('dtstart'),
				'end' : dat('dtend'),	
				'created' : dat('created'),
				'calendar' : c,
				}
			
			try:
				event = Event.objects.get(id = kwargs['id'])
				if event.sequence >= kwargs['sequence']:
					print "Skipping %s - Up to date event exists." % event
				else:
					print "Updating Event: %s " % event
					for k, v in kwargs.items():
						setattr(event, k, v)
					event.save()	

			except Event.DoesNotExist:
				event = Event(**kwargs)
				print "Creating Event: %s" % event
				event.save()
			
 
class Calendar(models.Model):
 	id = models.CharField(primary_key = True, max_length = 60)	
 	owner = models.ForeignKey(User, editable = False)
 	
 	urls = models.TextField(blank = True)
 
	style = models.TextField() 

	def cls(self):
		return self.id.replace(" ", "") 
	
	def __str__(self):
		return self.id 
 
 
class Event(models.Model):
	"""
	A Calendar Event.
	
	Modelled loosely around vEvent from rfc-2445.
	
	"""

 	id = models.CharField(primary_key = True, max_length = 60, editable = False)
 	
 	calendar = models.ForeignKey(Calendar)
 	
 	# Event Data
 	summary = models.TextField()
 	description = models.TextField()
 	status = models.TextField()
	
	location = models.TextField(blank = True)
	latitude = models.FloatField(blank = True)
	longitude = models.FloatField(blank = True)
	
	start = models.DateTimeField()
 	end = models.DateTimeField()
	
	# Event Object Metadata
	privacies = (
		("PUBLIC", "PUBLIC"),
		("PRIVATE", "PRIVATE"),
		("CONFIDENTIAL", "CONFIDENTIAL"),
	)
	privacy = models.CharField(choices = privacies, max_length = 20, default= "PUBLIC")# In RFC-2445 this is known as class
	
 	transp = models.TextField()
 	sequence = models.IntegerField()
 	

	
	created = models.DateTimeField(default = datetime.datetime.now(), editable = False)
	last_modified = models.DateTimeField(default = datetime.datetime.now())



	statuses = ( 
		("TENTATIVE", "TENTATIVE"),
		("CONFIRMED", "CONFIRMED"),
		("CANCELLED", "CANCELLED" ), 
	)
	status = models.CharField(choices = statuses, max_length = 20, blank = True)

	def __str__(self):
		return "Event:'%s' " % self.summary

	def form(self):
		import cal.forms
		return cal.forms.EventForm(instance = self)


class Todo(models.Model):
	"""
	A Todo list item.
	
	Specifies details about a single task.
	"""

	id = models.CharField(primary_key = True, max_length = 60, editable = False)	

	calendar = models.ForeignKey(Calendar)
	
	summary = models.TextField()
 	description = models.TextField()
 	location = models.TextField()
 	
 	statuses = ( 
		("NEEDS-ACTION", "NEEDS-ACTION"),
		("COMPLETED", "COMPLETED"),
		("IN-PROCESS", "IN-PROCESS"), 
		("CANCELLED", "CANCELLED" ), 
	)
 	status = models.CharField(choices = statuses, max_length = 20)
 	
 	
 	subsequent = models.ForeignKey('Todo', blank = True)
 	
 	due = models.DateTimeField(blank = True)
 	created = models.DateTimeField()
 	duration = models.FloatField(blank = True)
 	priority = models.IntegerField(default = 0)



class Agenda(object):
	"""
	Organise a user's tasks
	"""
	
	def __init__(self, user):
		self.user = user
	
	
	def items(self): 
 		now = datetime.datetime.now()
 		
 		itms = []
 		
 		for todo in Todo.objects.filter(calendar__owner = self.user, status = "COMPLETED"):
 			itms.append(todo)
 		
 		for event in Event.objects.filter(calendar__owner = self.user, start__gt = now).order_by('start'):
 			itms.append(event)
 		
 		return itms
 	
 	def __iter__(self):
 		for i in self.items():
 			yield i
 		

class Month(calendar.Calendar):
	startday = calendar.SUNDAY
	
	def __init__(self, year, month, owner):
		super(Month, self).__init__(self.startday)
		self.year = year
		self.month = month
		self.owner = owner

	def prev(self):
		if self.month >1:
			return Month(self.year, self.month - 1, self.owner)	
		return Month(self.year-1, 12)
	
	def next(self):
		if self.month <12:
			return Month(self.year, self.month + 1, self.owner)	
		return Month(self.year+1, 1)

	def name(self):
		return calendar.month_name[self.month]

	def day_names(self):
		return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

	def weeks(self):
		dts = self.monthdatescalendar(self.year, self.month)
		weeks = []
		for week in dts:
			wk = []
			
			for day in week:
				dy = {
					'date' : day,
					'is_today' : day == datetime.datetime.now().date(),
					'events' : Event.objects.filter(calendar__owner = self.owner, start__year = day.year, start__month = day.month, start__day = day.day).order_by('start'),
					'othermonth' : day.month != self.month,
				}
				
				wk.append(dy)
			weeks.append(wk)
		return weeks
		
	def get_absolute_url(self):
		return "%s/calendar/month/%s/%02d" % (settings.DOMAIN, self.year, self.month)		


class Day(object):
	def __init__(self, date):
		self.date = date
		self.is_today = self.date == datetime.datetime.now().date()	
		self.events = Event.objects.filter(start__year = date.year, start__month = date.month, start__day = date.day).order_by('start'),				