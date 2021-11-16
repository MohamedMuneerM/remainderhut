import arrow
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Remainder

# from twilio.rest import Client

@shared_task
def send_remainder(remainder_id):
	"""Send a remainder at scheduled time"""
	try:
		remainder = Remainder.objects.get(id=remainder_id)
	except Remainder.DoesNotExist:
		print("exp")

	# remainder_time = arrow.get(remainder.time).replace(tzinfo=tz.gettz(str(remainder.timezone)))
	# print(remainder_time)
	# subject = 'Hi You have an remainder coming up at {0}.'.format(
	#     remainder_time.format('h:mm a')
	# )
	subject = remainder.title
	message = remainder.description
	send_mail(subject, message, settings.EMAIL_HOST_USER, [remainder.user.email])
