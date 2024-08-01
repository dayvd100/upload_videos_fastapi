from celery import Celery

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

celery_app = Celery("worker", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
