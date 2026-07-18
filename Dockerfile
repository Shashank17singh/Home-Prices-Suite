FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server files
COPY server/ ./server/

# Set working directory to server so util.py and artifacts/ are found
WORKDIR /app/server

# Expose port
EXPOSE 5000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
