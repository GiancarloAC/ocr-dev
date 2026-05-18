import logging
import os
import torch
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router

# Configure PyTorch and NumPy threading BEFORE loading models
os.environ["OMP_NUM_THREADS"] = str(settings.TORCH_NUM_THREADS)
os.environ["OPENBLAS_NUM_THREADS"] = str(settings.TORCH_NUM_THREADS)
os.environ["MKL_NUM_THREADS"] = str(settings.TORCH_NUM_THREADS)
torch.set_num_threads(settings.TORCH_NUM_THREADS)
np.seterr(all='ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Open-source self-hosted OCR platform API.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up OpenOCR API...")
    logger.info(f"PyTorch threads: {settings.TORCH_NUM_THREADS}, Max upload: {settings.MAX_UPLOAD_SIZE_MB}MB")
    # Pre-load PaddleOCR model to avoid delay on first request
    try:
        from app.services.ocr_service import ocr_service
        logger.info("OCR Service initialized and model loaded.")
    except Exception as e:
        logger.error(f"Failed to initialize OCR Service: {str(e)}")
