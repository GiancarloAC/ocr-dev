import os
import tempfile
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.ocr import OCRResponse
from app.services.ocr_service import ocr_service

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]
ALLOWED_PDF_TYPES = ["application/pdf"]

@router.post("/image", response_model=OCRResponse)
async def process_image_endpoint(file: UploadFile = File(...)):
    """
    Process an uploaded image (PNG, JPG, JPEG) and extract text.
    """
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a JPEG or PNG image.")
    
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
    """
    if file.content_type not in ALLOWED_PDF_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF.")
        
    try:
        suffix = ".pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
            
        logger.info(f"Processing uploaded PDF: {file.filename}")
        
        # Run OCR
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
