import settings

def glob(request):
	return {
		'MEDIA' : settings.MEDIA,
	}