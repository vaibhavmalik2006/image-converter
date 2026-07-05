import os
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import get_db
from models.history import ProcessingHistory
from services.image_service import get_image_format, process_image, validate_image
from utils.file_utils import create_temp_file, get_temp_path

MEDIA_TYPES = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
    "BMP": "image/bmp",
    "GIF": "image/gif",
    "TIFF": "image/tiff",
    "ICO": "image/x-icon",
}

router = APIRouter()


@router.get("/")
def root():
    return {"message": "AI Image Converter API is running"}


@router.post("/upload")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not validate_image(file.filename or ""):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_id, temp_path, _ = create_temp_file(file.filename or "image")
    with temp_path.open("wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "id": file_id,
        "filename": file.filename,
        "format": get_image_format(temp_path),
        "path": str(temp_path),
    }


@router.post("/convert")
async def convert_image(
    file_id: str = Query(...),
    output_format: str = Query(...),
    width: int | None = Query(None),
    height: int | None = Query(None),
    keep_aspect_ratio: bool = Query(True),
    dpi: int | None = Query(None),
    quality: int = Query(90),
    target_size_kb: float | None = Query(None),
    db: Session = Depends(get_db),
):
    input_path = get_temp_path(file_id)
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    original_format = get_image_format(input_path)
    data, final_format, out_width, out_height, _ = process_image(
        input_path=input_path,
        output_format=output_format,
        width=width,
        height=height,
        keep_aspect_ratio=keep_aspect_ratio,
        dpi=dpi,
        quality=quality,
        target_size_kb=target_size_kb,
    )

    media_type = MEDIA_TYPES.get(final_format.upper(), "application/octet-stream")
    extension = final_format.lower()
    if extension == "jpeg":
        extension = "jpg"
    headers = {
        "Content-Disposition": f"attachment; filename=converted.{extension}"
    }
    response = Response(content=data, media_type=media_type, headers=headers)

    history = ProcessingHistory(
        filename=f"{file_id}.{original_format.lower()}",
        original_format=original_format,
        converted_format=final_format,
        original_size=os.path.getsize(input_path) / 1024,
        final_size=len(data) / 1024,
        width=out_width,
        height=out_height,
        dpi=dpi or 72,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return response


@router.post("/resize")
async def resize_image(
    file_id: str = Query(...),
    width: int = Query(...),
    height: int = Query(...),
    keep_aspect_ratio: bool = Query(True),
    output_format: str = Query("PNG"),
    dpi: int | None = Query(None),
    quality: int = Query(90),
):
    input_path = get_temp_path(file_id)
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    data, final_format, out_width, out_height, _ = process_image(
        input_path=input_path,
        output_format=output_format,
        width=width,
        height=height,
        keep_aspect_ratio=keep_aspect_ratio,
        dpi=dpi,
        quality=quality,
    )
    media_type = MEDIA_TYPES.get(final_format.upper(), "application/octet-stream")
    response = Response(content=data, media_type=media_type)
    extension = final_format.lower()
    if extension == "jpeg":
        extension = "jpg"
    response.headers["Content-Disposition"] = f"attachment; filename=resized.{extension}"
    return response


@router.post("/compress")
async def compress_image(
    file_id: str = Query(...),
    quality: int = Query(90),
    target_size_kb: float | None = Query(None),
    output_format: str = Query("JPEG"),
    dpi: int | None = Query(None),
):
    input_path = get_temp_path(file_id)
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    data, final_format, _, _, _ = process_image(
        input_path=input_path,
        output_format=output_format,
        dpi=dpi,
        quality=quality,
        target_size_kb=target_size_kb,
    )
    media_type = MEDIA_TYPES.get(final_format.upper(), "application/octet-stream")
    response = Response(content=data, media_type=media_type)
    extension = final_format.lower()
    if extension == "jpeg":
        extension = "jpg"
    response.headers["Content-Disposition"] = f"attachment; filename=compressed.{extension}"
    return response


@router.post("/change-dpi")
async def change_dpi(
    file_id: str = Query(...),
    dpi: int = Query(...),
    output_format: str = Query("PNG"),
    quality: int = Query(90),
):
    input_path = get_temp_path(file_id)
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    data, final_format, _, _, _ = process_image(
        input_path=input_path,
        output_format=output_format,
        dpi=dpi,
        quality=quality,
    )
    media_type = MEDIA_TYPES.get(final_format.upper(), "application/octet-stream")
    response = Response(content=data, media_type=media_type)
    extension = final_format.lower()
    if extension == "jpeg":
        extension = "jpg"
    response.headers["Content-Disposition"] = f"attachment; filename=dpi.{extension}"
    return response


@router.get("/download/{file_id}")
async def download_file(
    file_id: str,
    output_format: str = Query("PNG"),
    width: int | None = Query(None),
    height: int | None = Query(None),
    keep_aspect_ratio: bool = Query(True),
    dpi: int | None = Query(None),
    quality: int = Query(90),
    target_size_kb: float | None = Query(None),
    db: Session = Depends(get_db),
):
    input_path = get_temp_path(file_id)
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    original_format = get_image_format(input_path)
    data, final_format, out_width, out_height, _ = process_image(
        input_path=input_path,
        output_format=output_format,
        width=width,
        height=height,
        keep_aspect_ratio=keep_aspect_ratio,
        dpi=dpi,
        quality=quality,
        target_size_kb=target_size_kb,
    )
    extension = final_format.lower()
    if extension == "jpeg":
        extension = "jpg"
    media_type = MEDIA_TYPES.get(final_format.upper(), "application/octet-stream")

    response = Response(content=data, media_type=media_type)
    response.headers["Content-Disposition"] = f"attachment; filename=processed.{extension}"

    history = ProcessingHistory(
        filename=f"{file_id}.{original_format.lower()}",
        original_format=original_format,
        converted_format=final_format,
        original_size=os.path.getsize(input_path) / 1024,
        final_size=len(data) / 1024,
        width=out_width,
        height=out_height,
        dpi=dpi or 72,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return response
