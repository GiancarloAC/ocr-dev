# OpenOCR Backend API

A production-ready, self-hosted OCR platform backend powered by FastAPI, PaddleOCR, and PyMuPDF.

## Features
- **Image OCR**: Process PNG, JPG, JPEG files.
- **PDF OCR**: Handle multi-page PDFs using PyMuPDF and PaddleOCR.
- **Structured Data Extraction**: Returns raw text and structured bounding box/confidence data.
- **Singleton Model**: Efficient OCR processing without reloading the model.
- **Docker-Ready**: Easy deployment with Docker.

## Architecture
The application follows a clean architecture model:

- `app/api/`: FastAPI routers and endpoints.
- `app/core/`: Application configuration and settings.
- `app/schemas/`: Pydantic models for request/response validation.
- `app/services/`: Core business logic (OCR processing).
- `app/utils/`: Helper utilities (e.g., PDF to Image conversion).

## Getting Started

### Local Setup (Without Docker)

1. **Install dependencies**:
   Ensure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```
   *Note: For PaddleOCR, you may need system libraries like `libgl1-mesa-glx` and `libglib2.0-0`.*

2. **Environment Variables**:
   Copy `.env.example` to `.env` and adjust settings as needed.
   ```bash
   cp .env.example .env
   ```

3. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup

1. **Build the image**:
   ```bash
   docker build -t openocr-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 --env-file .env.example openocr-api
   ```

## API Documentation
Once the server is running, you can access the interactive Swagger documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
