import settings
import datetime

def glob(request):
	return {
		'MEDIA' : settings.MEDIA,
		'now' : datetime.datetime.now(),
	}