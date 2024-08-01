from celery import Celery
from database.database import SessionLocal
from crud import create_video

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

celery_app = Celery("worker", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery_app.task()
def process_upload(file_path: str, title: str, description: str, ext: str):
    db = SessionLocal()
    try:
        create_video(db, title=title, description=description, ext=ext)
    finally:
        db.close()

    return {
        "file_path": file_path,
        "title": title,
        "description": description,
        "ext": ext,
        "message": "File processed successfully",
    }
