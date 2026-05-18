import logging
import os
import tempfile
from typing import Dict, Any
import easyocr
from app.core.config import settings
from app.utils.pdf_utils import convert_pdf_to_images

logger = logging.getLogger(__name__)

class OCRService:
    _instance = None
    _ocr_model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRService, cls).__new__(cls)
            cls._instance._initialize_model()
        return cls._instance

    def _initialize_model(self):
        """Initialize EasyOCR singleton instance"""
        logger.info(f"Initializing EasyOCR (Lang: {settings.OCR_LANG}, GPU: {settings.USE_GPU})")
        
        # EasyOCR expects a list of language codes
        lang_code = settings.OCR_LANG if settings.OCR_LANG else 'en'
        # Convert paddle 'en' or similar to easyocr 'en'
        # Luckily 'en', 'es', 'fr' etc map identically in both usually.
        langs = [lang_code]
        
        self._ocr_model = easyocr.Reader(
            lang_list=langs,
            gpu=settings.USE_GPU
        )
        logger.info("EasyOCR model initialized successfully.")

    def process_image(self, image_path: str) -> Dict[str, Any]:
        """Process a single image and extract text and structured data"""
        logger.info(f"Processing image: {image_path}")
        try:
            # EasyOCR returns: [([[x1,y1], [x2,y2], [x3,y3], [x4,y4]], 'text', confidence), ...]
            result = self._ocr_model.readtext(image_path)
            
            raw_text = ""
            structured_data = []
            
            for line in result:
                # Format box points to regular floats for JSON serialization
                box = [[float(point[0]), float(point[1])] for point in line[0]]
                text = str(line[1])
                confidence = float(line[2])
                
                raw_text += text + "\n"
                structured_data.append({
                    "text": text,
                    "confidence": confidence,
                    "box": box
                })
            
            return {
                "raw_text": raw_text.strip(),
                "structured_data": structured_data
            }
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Process a multi-page PDF document"""
        logger.info(f"Processing PDF: {pdf_path}")
        
        pages_result = []
        full_raw_text = ""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Convert PDF to images
                image_paths = convert_pdf_to_images(pdf_path, temp_dir)
                
                # Process each page image
                for i, img_path in enumerate(image_paths):
                    page_res = self.process_image(img_path)
                    
                    pages_result.append({
                        "page_number": i + 1,
                        "raw_text": page_res["raw_text"],
                        "structured_data": page_res["structured_data"]
                    })
                    
                    full_raw_text += f"--- Page {i + 1} ---\n"
                    full_raw_text += page_res["raw_text"] + "\n\n"
                    
            except Exception as e:
                logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
                raise
                
        return {
            "raw_text": full_raw_text.strip(),
            "pages": pages_result
        }

# Singleton instance
ocr_service = OCRService()
