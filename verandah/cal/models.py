import datetime
import calendar
import urllib

from django.db import models

import icalendar 


def parse_iCal(url):
	calendar = urllib.urlopen(url)
	cal = icalendar.Calendar.from_string(calendar.read())
	c = Calendar(
		id = cal.decoded('X-WR-CALNAME')
	)
	c.save()
	
	for component in cal.walk():
		if component.name == 'VEVENT':
			
			def dat(param):
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
			if Event.objects.filter(id = kwargs['id']):
				print "Skipping - Event exists"
				continue
			e = Event(**kwargs)
			print e
			e.save()
			
 
class Calendar(models.Model):
 	id = models.CharField(primary_key = True, max_length = 60)	
 
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


class Month(calendar.Calendar):
	startday = calendar.SUNDAY
	
	def __init__(self, year, month):
		super(Month, self).__init__(self.startday)
		self.year = year
		self.month = month


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
					'events' : Event.objects.filter(start__year = day.year, start__month = day.month, start__day = day.day).order_by('start')
				}
				
				wk.append(dy)
			weeks.append(wk)
		return weeks
		
		
				