import logging
from typing import Tuple
import pdfplumber
import pypdf

logger = logging.getLogger(__name__)


def extract_text_pdfplumber(pdf_path: str) -> Tuple[str, int]:
    """
    Extract text from PDF using pdfplumber (faster, layout-aware).
    
    Returns:
        Tuple[full_text, page_count]
    """
    try:
        full_text = ""
        page_count = 0
        
        with pdfplumber.open(pdf_path) as pdf:
            page_count = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                if text.strip():
                    full_text += f"--- Page {i + 1} ---\n{text}\n\n"
        
        logger.info(f"Extracted {len(full_text)} chars from {page_count} pages using pdfplumber")
        return full_text.strip(), page_count
    
    except Exception as e:
        logger.warning(f"pdfplumber extraction failed: {str(e)}")
        return "", 0


def extract_text_pypdf(pdf_path: str) -> Tuple[str, int]:
    """
    Extract text from PDF using pypdf (fallback).
    
    Returns:
        Tuple[full_text, page_count]
    """
    try:
        full_text = ""
        
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            page_count = len(reader.pages)
            
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    full_text += f"--- Page {i + 1} ---\n{text}\n\n"
        
        logger.info(f"Extracted {len(full_text)} chars from {page_count} pages using pypdf")
        return full_text.strip(), page_count
    
    except Exception as e:
        logger.warning(f"pypdf extraction failed: {str(e)}")
        return "", 0


def extract_text_from_pdf(pdf_path: str) -> Tuple[str, int]:
    """
    Try to extract text from PDF using multiple methods.
    Falls back from pdfplumber → pypdf.
    
    Returns:
        Tuple[extracted_text, page_count]
    """
    logger.info(f"Attempting text extraction from PDF: {pdf_path}")
    
    # Try pdfplumber first (better layout handling)
    text, page_count = extract_text_pdfplumber(pdf_path)
    if text:
        logger.info("✓ Text extracted via pdfplumber")
        return text, page_count
    
    # Fallback to pypdf
    text, page_count = extract_text_pypdf(pdf_path)
    if text:
        logger.info("✓ Text extracted via pypdf (fallback)")
        return text, page_count
    
    logger.warning("✗ No text extracted from PDF - likely scanned or corrupted")
    return "", page_count
