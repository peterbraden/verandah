from django.forms import ModelForm, CharField, Textarea

from datetime import datetime

import typewriter.models


class DocumentForm(ModelForm):
	content = CharField(widget=Textarea)
	comment = CharField(widget=Textarea, required = False)	

	class Meta:
		model = typewriter.models.Document
		fields = ('name', 'content')
		
	def save(self):
		doc = super(DocumentForm, self).save(commit = False)
		
		doc.owner = self.owner
		doc.save()

		rev = typewriter.models.Revision(
			doc = doc,
			date = datetime.now(),
			content = self.cleaned_data['content'],
			comment = self.cleaned_data['comment']
		)
		
		try:
			rev.prev_revision = doc.current
		except typewriter.models.Revision.DoesNotExist:
			pass

		rev.save()
		doc.current = rev
		doc.save()