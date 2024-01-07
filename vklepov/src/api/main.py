"""FastAPI router module."""
from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from ultralytics import YOLO
from ultralytics.data.loaders import LoadImages
from tempfile import NamedTemporaryFile
from . import schemas

app = FastAPI()
app.mount("/app", StaticFiles(directory="front/dist", html=True), name="static")
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

model = YOLO("./yolov8s_traffic.pt")

storage: dict[schemas.VideoDetection] = {}


def process_video(filename: str, id: str):
    try:
        results = model(filename, stream=True)

        total_frames = 0
        for _f in LoadImages(filename):
            total_frames += 1
        storage[id] = schemas.VideoDetection(total_frames=total_frames)

        for num_frame, result in enumerate(results):
            objects = []
            for i, cls in enumerate(result.boxes.cls.tolist()):
                objects.append(
                    schemas.DetectionBox(
                        cls=result.names[cls],
                        confidence=result.boxes.conf[i].item(),
                        coords=result.boxes.xyxyn[i].tolist(),
                    )
                )
            storage[id].frames.append(
                schemas.Frame(objects=objects, num_frame=num_frame)
            )
    finally:
        Path(filename).unlink()


@app.post("/detection/{id}")
async def upload_video(file: UploadFile, id: str, bg: BackgroundTasks):
    """Run CV on video."""
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile("wb", delete=False, suffix=suffix) as temp:
            contents = await file.read()
            temp.write(contents)
            bg.add_task(process_video, temp.name, id)
    except Exception:
        raise HTTPException(500)
    finally:
        await file.close()

    return {}


@app.get("/detection/{id}")
async def get_video(id: str, skip: int = 0) -> schemas.VideoDetection:
    """Get video status by id."""
    if id not in storage:
        raise HTTPException(404)
    detection = storage.get(id)
    frames_page = [f for f in detection.frames if f.num_frame > skip]
    return schemas.VideoDetection(
        total_frames=detection.total_frames, frames=frames_page
    )
