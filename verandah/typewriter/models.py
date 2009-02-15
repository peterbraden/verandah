from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
	name = models.CharField(max_length = 60)
	
	owner = models.ForeignKey(User)
	
	current = models.ForeignKey('Revision', blank = True, null = True)

	content = models.TextField()

	def __str__(self):
		return "Document:%s" % self.name
	
	
class Revision(models.Model):
	doc = models.ForeignKey(Document)
	prev_revision = models.ForeignKey('Revision', blank = True, null = True)
	
	date = models.DateTimeField()
	content = models.TextField()
	comment = models.TextField(blank = True)	
	
	def __str__(self):
		return "Revision:%s(%s)" % (self.id, self.doc.name)