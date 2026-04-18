# Build Stage: Compile C++ Engine
FROM gcc:latest as builder
WORKDIR /app
COPY scheduler.cpp .
RUN g++ -O3 scheduler.cpp -o scheduler

# Production Stage: Python Flask
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Copy compiled C++ binary from builder stage
COPY --from=builder /app/scheduler ./build/scheduler

# Set environment variables
ENV PORT=8080
ENV FLASK_ENV=production

# Run the application
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
