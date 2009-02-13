from django.core.management.base import LabelCommand

import cal.models


class Command(LabelCommand):
	help = "Get some calendars off the internets"

	requires_model_validation = False
	
	def handle_label(self, label, **options):
		cal.models.parse_iCal(label)
		