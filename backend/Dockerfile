FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Instalar PyTorch CPU antes de las dependencias que lo necesiten
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch torchvision

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
