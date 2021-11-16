import arrow
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from timezone_field import TimeZoneField
from django.db.models.signals import (
    pre_save,
)
from django.dispatch import receiver
from celery.result import AsyncResult

class User(AbstractUser):
	""" custom user model extends from abstract user """
	email = models.EmailField(_('email address'), unique=True, blank=True)
	# USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['email']
	is_subcribed = False


class Remainder(models.Model):
	""" Remainder class where users schedule their remainders """

	# add "email field/email list" to send to send after proper research (it may lead to spam)
	# current idea is to send to the created users email address
	user =  models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=1000)
	description = models.TextField(null=True, blank=True)
	time_zone = TimeZoneField(default='US/Pacific')
	when = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	modified_at = models.DateTimeField(auto_now=True, editable=False)
	is_repetitive = models.BooleanField(default=False)
	# phone numbers must be otp verified
	send_sms = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Remainder"
		verbose_name_plural = "Remainders"

	def __str__(self):
		return self.title
	
	def clean(self):
		"""Checks that remainder are not scheduled in the past"""
		remainder_time = arrow.get(self.when, self.time_zone.zone)
		if remainder_time < arrow.utcnow():
			raise ValidationError(
				'You cannot schedule an remainder for the past. Please check your time and time_zone')
			
	@property
	def is_success(self):
		return self.remaindertask.is_success

	def schedule_reminder(self):
		"""Schedules a Celery task to send a reminder about this remainder"""

		# Calculate the correct time to send this reminder
		remainder_time = arrow.get(self.when, self.time_zone.zone)
		# reminder_time = remainder_time.replace(minutes=-settings.REMINDER_TIME)

		# Schedule the Celery task
		# import statement is here for avoiding circular imports
		from .tasks import send_remainder
		from remainderhut.celery import error_handler
		schd = send_remainder.apply_async((self.pk,), eta=remainder_time, link_error=error_handler.s())
		return schd


	def save(self, *args, **kwargs):
		"""Custom save method which also schedules a reminder"""

		# Save our remainder, which populates self.pk,
		# which is used in schedule_reminder
		super(Remainder, self).save(*args, **kwargs)

		# Schedule a new reminder task for this remaninder obj
		schedule_obj = self.schedule_reminder()

		RemainderTask.objects.create(
			remainder=self,
			task_id=schedule_obj.task_id
		)

class RemainderTask(models.Model):
	remainder = models.OneToOneField(Remainder, on_delete=models.CASCADE)
	task_id = models.CharField(max_length=999)

	@property
	def is_success(self):
		return AsyncResult(self.task_id).successful()

	def __str__(self):
		return self.task_id

# @receiver(pre_save, sender=Remainder)
# def remainder_pre_save_receiver(sender, instance, *args, **kwargs):
#     """
#     before saved in the database
#     """
#     # a = instance.schedule_reminder()
#     # print(a)
#     print(instance.id) # None