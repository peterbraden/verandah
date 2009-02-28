import datetime
import calendar
import urllib

from django.db import models
from django.contrib.auth.models import User

import settings
import icalendar 


def parse_iCal(url, owner):
	calendar = urllib.urlopen(url)
	cal = icalendar.Calendar.from_string(calendar.read())
	
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
 
class Event(models.Model):
 	id = models.CharField(primary_key = True, max_length = 60)
 	
 	calendar = models.ForeignKey(Calendar)
 	
 	summary = models.TextField()
 	description = models.TextField()
 	status = models.TextField()
	location = models.TextField()
	
 	transp = models.TextField()
 	cls =  models.TextField()
 	sequence = models.IntegerField()
 	
 	start = models.DateTimeField()
 	end = models.DateTimeField()
	
	created = models.DateTimeField()

	def __str__(self):
		return "Event:'%s' " % self.summary

class Month(calendar.Calendar):
	startday = calendar.SUNDAY
	
	def __init__(self, year, month):
		super(Month, self).__init__(self.startday)
		self.year = year
		self.month = month


	def prev(self):
		if self.month >1:
			return Month(self.year, self.month - 1)	
		return Month(self.year-1, 12)
	
	def next(self):
		if self.month <12:
			return Month(self.year, self.month + 1)	
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
					'events' : Event.objects.filter(start__year = day.year, start__month = day.month, start__day = day.day).order_by('start'),
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