import os

from celery import Celery
from django.conf import settings 

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remainderhut.settings')

app = Celery('remainderhut', broker=settings.CELERY_BROKER_URL)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.task
def error_handler(request, exc, traceback):
	print('Task {0} raised exception: {1!r}\n{2!r}'.format(
		  request.id, exc, traceback))
