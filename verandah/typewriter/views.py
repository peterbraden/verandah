from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

import typewriter.models
from typewriter.forms import DocumentForm


@login_required
def dashboard(request):
	context = {
		'documents' : typewriter.models.Document.objects.all()
	}
	return HttpResponse(get_template("typewriter_dashboard.html").render(RequestContext(request, context)))	


@login_required
def document(request, document_name = None):
	document = None
	
	if request.POST:
		form = DocumentForm(request.POST)
		form.owner = request.user
		
		if form.is_valid():
			form.save()
			print "Form Saved"
		else:
			print "Errors: ", form.errors, form.__dict__
	else:	
		if document_name:
			document = get_object_or_404(typewriter.models.Document, name = document_name)
			form = DocumentForm(instance=document)
		else:
			form = DocumentForm()
	
	context = {
		'form' : form,
		'document' : document
	}
	
	return HttpResponse(get_template("typewriter_document.html").render(RequestContext(request, context)))
