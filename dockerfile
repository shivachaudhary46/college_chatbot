FROM python:3.11
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/app ./app
COPY backend/data ./data

# Expose backend to 8000 ports
EXPOSE 8000

# Setup an app user so the 
RUN useradd app
USER app 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]