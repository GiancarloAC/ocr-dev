import fitz  # PyMuPDF
import os
import logging
from typing import List

logger = logging.getLogger(__name__)

def convert_pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 200) -> List[str]:
    """
    Convert a PDF file to a list of image file paths using PyMuPDF.
    """
    image_paths = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=dpi, alpha=False)

            image_path = os.path.join(output_dir, f"page_{page_num}.png")
            pix.save(image_path)
            image_paths.append(image_path)
            logger.debug(f"Saved page {page_num} to {image_path}")
    except Exception as e:
        logger.error(f"Failed to convert PDF to images: {str(e)}")
        raise
    finally:
        if 'doc' in locals():
            doc.close()
            
    return image_paths
