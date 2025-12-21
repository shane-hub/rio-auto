from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "rio_auto",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

if settings.CELERY_TASK_ALWAYS_EAGER:
    celery_app.conf.task_always_eager = True

celery_app.conf.task_routes = {
    "app.services.task_runner.run_task_celery": "main-queue",
}
