import os
import tempfile
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.ocr import OCRResponse
from app.services.ocr_service import ocr_service
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]
ALLOWED_PDF_TYPES = ["application/pdf"]
MAX_FILE_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024  # Convert to bytes

async def validate_file_size(file: UploadFile) -> None:
    """Validate that uploaded file doesn't exceed size limit."""
    # Read file in chunks to get size without loading everything in memory
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB chunks
    
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE_MB}MB"
            )
    
    # Reset file pointer
    await file.seek(0)

@router.post("/image", response_model=OCRResponse)
async def process_image_endpoint(file: UploadFile = File(...)):
    """
    Process an uploaded image (PNG, JPG, JPEG) and extract text.
    """
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a JPEG or PNG image.")
    
    # Validate file size
    await validate_file_size(file)
    
    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
            
        logger.info(f"Processing uploaded image: {file.filename}")
        
        # Run OCR
        result = ocr_service.process_image(temp_path)
        
        # Clean up temp file
        os.remove(temp_path)
        
        return OCRResponse(
            filename=file.filename,
            content_type=file.content_type,
            raw_text=result["raw_text"],
            structured_data=result["structured_data"]
        )
    except Exception as e:
        logger.error(f"Error in process_image_endpoint: {str(e)}")
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@router.post("/pdf", response_model=OCRResponse)
async def process_pdf_endpoint(file: UploadFile = File(...)):
    """
    Process an uploaded multi-page PDF and extract text.
    
    Strategy:
    1. Attempt text extraction (fast, low memory)
    2. Validate extracted text quality
    3. Fallback to OCR only if needed (escaneado/invalido)
    """
    if file.content_type not in ALLOWED_PDF_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF.")
    
    # Validate file size
    await validate_file_size(file)
        
    try:
        suffix = ".pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
            
        logger.info(f"Processing uploaded PDF: {file.filename}")
        
        # Process PDF (with smart extraction first)
        result = ocr_service.process_pdf(temp_path)
        
        # Clean up temp file
        os.remove(temp_path)
        
        return OCRResponse(
            filename=file.filename,
            content_type=file.content_type,
            raw_text=result["raw_text"],
            pages=result["pages"]
        )
    except Exception as e:
        logger.error(f"Error in process_pdf_endpoint: {str(e)}")
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"PDF OCR processing failed: {str(e)}")
