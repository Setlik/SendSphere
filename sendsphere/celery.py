import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sendsphere.settings")

app = Celery("sendsphere")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    task_acks_late=False,
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    broker_transport_options={"visibility_timeout": 3600},
)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
