FROM python:3.11
WORKDIR /backend/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code 
COPY src ./source
EXPOSE 8000

# Setup an app user so the 
RUN useradd app
USER app 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]