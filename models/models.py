from sqlalchemy import VARCHAR, Column, Integer, String

from database.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(255), nullable=True)
    description = Column(String, nullable=True)
    ext = Column(VARCHAR(15))
