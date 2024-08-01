from sqlalchemy.orm import Session
from models.models import Video
import logging

logger = logging.getLogger(__name__)


def create_video(db: Session, title: str, description: str, ext: str):
    try:
        db_video = Video(title=title, description=description, ext=ext)
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        logger.info(f"Video created: {db_video.id}")
        return db_video
    except Exception as e:
        logger.error(f"Error creating video: {e}")
        db.rollback()
        raise


def list_all_videos(db: Session):
    return db.query(Video).all()


def delete_video(db: Session, id: int):
    db_video = db.query(Video).filter(Video.id == id).first()

    if db_video:
        db.delete(db_video)
        db.commit()
        db.refresh(db_video)
        return db_video

    else:
        return None
