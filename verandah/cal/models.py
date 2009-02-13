import datetime
import calendar
import urllib

from django.db import models

import icalendar 


def parse_iCal(url):
	calendar = urllib.urlopen(url)
	cal = lib.icalendar.Calendar.from_string(calendar.read())
	print cal
 
class Calendar(models.Model):
 	id = models.CharField(primary_key = True, max_length = 60)	
 
class Event(models.Model):
 	id = models.CharField(primary_key = True, max_length = 60)
 	
 	calendar = models.ForeignKey(Calendar)
 	
 	summary = models.TextField()
 	
 	start = models.DateTimeField()
 	finish = models.DateTimeField()



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
				}
				
				wk.append(dy)
			weeks.append(wk)
		return weeks
		
		
				