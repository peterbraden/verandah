from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, Http404, HttpResponseRedirect


def homepage(request):
	return HttpResponse(get_template('home.html').render(RequestContext(request, {})))