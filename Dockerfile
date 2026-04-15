# 1. Use a lightweight Python base image
FROM python:3.10-slim

# 2. SENIOR FIX: Install system libraries required by OpenCV (cv2)
# Without these, cv2 will instantly crash in a blank Linux container.
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy your requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your actual Python code into the container
COPY . .

# 6. Expose Port 7860 (Hugging Face strictly requires this exact port)
EXPOSE 7860

# 7. Start Gunicorn, binding to HF's required port with our 300s timeout
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "300", "app:app"]
