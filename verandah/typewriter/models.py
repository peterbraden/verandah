from django.db import models



class Document(models.Model):
	name = models.CharField(max_length = 60)
	
	owner = models.ForeignKey(User)