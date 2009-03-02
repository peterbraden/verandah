from django.forms import ModelForm, URLField, ChoiceField

import cal.models
import hashlib
import datetime

class CalendarForm(ModelForm):
	urls = URLField(help_text = "URL to an ical calendar (.ics)")
	
	STYLES = [
		('color:#900;background-color:#e99;', 'Red'),
		('color:#ec9;background-color:#950;', 'Orange'),
		('color:#980;background-color:#ee9;', 'Yellow'),
		('color:#090;background-color:#9e9;', 'Green'),
		('color:#009;background-color:#ffe;', 'Blue'),
		('color:#509;background-color:#c9e;', 'Purple'),
		('color:#fff;background-color:#555;', 'Grey'),
	]

	style = ChoiceField(help_text = "Colours to use for this calendar", choices = STYLES)
	
	
	class Meta:
		model = cal.models.Calendar

class EventForm(ModelForm):
	class Meta:
		model = cal.models.Event
		exclude = ['transp', 'sequence', 'last_modified', 'priority']
	
	def save(self):
		event =  super(EventForm, self).save(commit = False)
		event.id = "%s%s" % (hashlib.sha1("%s%s" % (event.calendar.owner.username, datetime.datetime.now())).hexdigest(), "@verandah")	
		event.save()