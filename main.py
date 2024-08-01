from fastapi import FastAPI, UploadFile, File, Depends
from secrets import token_hex
import uvicorn
from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.models import Video
from crud import list_all_videos, delete_video
import os
from tasks.tasks import process_upload

app = FastAPI(title="Upload videos here")

Video.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


@app.get("/")
def home_videos(db: Session = Depends(get_db)):
    return list_all_videos(db)


@app.delete("/delete")
def delete_video_home(
    id: int,
    db: Session = Depends(get_db),
):
    delete_video(db, id=id)


@app.post("/upload_files")
async def upload_files(
    file: UploadFile = File(...), description: str = "", db: Session = Depends(get_db)
):
    file_ext = file.filename.split(".").pop()
    file_name = token_hex(10)
    file_path = f"{file_name}.{file_ext}"

    file_path = os.path.join("downloads", file_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    tasks = process_upload.delay(file_path, file_name, description, file_ext)

    return {
        "Sucess": True,
        "file_path": file_path,
        "task_id": tasks.id,
        "message": "File uploaded successfully",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
