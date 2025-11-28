from fastapi import APIRouter, UploadFile, File,status,Request
import os
import shutil
from src.prasad.images.model.image_model import ImageModel

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload-image",status_code=status.HTTP_201_CREATED)
async def upload_to_subfolder(request:Request,image: UploadFile = File(...)):
    UPLOAD_DIR ="src/prasad/static/uploads"

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    base_url = str(request.base_url).rstrip("/")

    image_url = f"{base_url}/static/uploads/{image.filename}"

    new_image_model = ImageModel(
        image_url=image_url,
    )
    await new_image_model.insert()
    return new_image_model





async def upload_image(request:Request,image: UploadFile = File(...)) ->str:
    UPLOAD_DIR ="src/prasad/static/uploads"

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    base_url = str(request.base_url).rstrip("/")

    image_url = f"{base_url}/static/uploads/{image.filename}"

    new_image_model = ImageModel(
        image_url=image_url,
    )
    await new_image_model.insert()
    return image_url