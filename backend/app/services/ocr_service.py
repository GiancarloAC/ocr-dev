import logging
import os
import tempfile
import gc
from typing import Dict, Any, Tuple
import easyocr
from app.core.config import settings
from app.utils.pdf_utils import convert_pdf_to_images
from app.utils.pdf_extraction import extract_text_from_pdf
from app.utils.text_validation import validate_extracted_text, is_pdf_likely_scanned
from app.utils.memory_profiler import log_memory_checkpoint

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
            
            # Cleanup
            del result
            gc.collect()
            
            return {
                "raw_text": raw_text.strip(),
                "structured_data": structured_data
            }
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process a multi-page PDF document.
        
        Strategy:
        1. Try extract_text_from_pdf() first
        2. Validate extracted text (heuristics)
        3. If valid and not scanned -> use extracted text
        4. If invalid or scanned -> fallback to OCR
        """
        logger.info(f"Processing PDF: {pdf_path}")
        log_memory_checkpoint("START process_pdf")
        
        # Step 1: Try extraction
        extracted_text, page_count = extract_text_from_pdf(pdf_path)
        log_memory_checkpoint("AFTER text_extraction")
        
        # Step 2: Validate extraction
        is_valid, confidence, reason = validate_extracted_text(extracted_text, lang=settings.OCR_LANG)
        is_scanned, scan_confidence = is_pdf_likely_scanned(extracted_text, page_count)
        
        logger.info(f"Extraction validation: valid={is_valid}, confidence={confidence:.2%}, reason={reason}")
        logger.info(f"PDF likely scanned: {is_scanned}, scan_confidence={scan_confidence:.2%}")
        
        # Step 3: If text is valid and PDF is not scanned, use extraction
        if is_valid and not is_scanned:
            logger.info("✓ Using extracted text (no OCR needed)")
            log_memory_checkpoint("TEXT_EXTRACTION_SUCCESS")
            # Parse pages from extracted text
            pages_result = self._parse_extracted_pages(extracted_text)
            return {
                "raw_text": extracted_text,
                "pages": pages_result,
                "extraction_method": "text_extraction",
                "processed_via_ocr": False
            }
        
        # Step 4: Fallback to OCR
        logger.info("→ Fallback to OCR (extracted text invalid or PDF is scanned)")
        log_memory_checkpoint("BEFORE OCR_FALLBACK")
        result = self._process_pdf_with_ocr(pdf_path)
        log_memory_checkpoint("END process_pdf")
        return result

    def _parse_extracted_pages(self, extracted_text: str) -> list:
        """
        Parse extracted text back into page-based structure.
        Expected format: "--- Page N ---\ntext\n\n"
        """
        pages_result = []
        current_page = 1
        current_text = ""
        
        lines = extracted_text.split('\n')
        for line in lines:
            if line.startswith("--- Page"):
                if current_text.strip():
                    pages_result.append({
                        "page_number": current_page,
                        "raw_text": current_text.strip(),
                        "structured_data": []  # No structured data from text extraction
                    })
                    current_page += 1
                    current_text = ""
            else:
                current_text += line + "\n"
        
        # Don't forget last page
        if current_text.strip():
            pages_result.append({
                "page_number": current_page,
                "raw_text": current_text.strip(),
                "structured_data": []
            })
        
        return pages_result

    def _process_pdf_with_ocr(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process PDF pages via OCR (called as fallback).
        Page-by-page processing to minimize memory usage.
        """
        pages_result = []
        full_raw_text = ""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Convert PDF to images
                image_paths = convert_pdf_to_images(pdf_path, temp_dir)
                log_memory_checkpoint(f"AFTER pdf_to_images ({len(image_paths)} pages)")
                
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
                    
                    # Explicit cleanup to reduce memory usage
                    del page_res
                    gc.collect()
                    log_memory_checkpoint(f"AFTER page {i + 1} cleanup")
                    
            except Exception as e:
                logger.error(f"Error processing PDF {pdf_path} with OCR: {str(e)}")
                raise
        
        return {
            "raw_text": full_raw_text.strip(),
            "pages": pages_result,
            "extraction_method": "ocr",
            "processed_via_ocr": True
        }

# Singleton instance
ocr_service = OCRService()
