from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from datetime import datetime

import cal.models
import typewriter.models

@login_required
def homepage(request):


	context = {
		'day' : cal.models.Day(datetime.today()),
		'documents' : typewriter.models.Document.objects.filter(owner = request.user) 
	}
	
	return HttpResponse(get_template('home.html').render(RequestContext(request, context)))