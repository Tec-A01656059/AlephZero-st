# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements if present, else fallback to install streamlit only
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir streamlit

# Copy all app files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Set Streamlit to listen on all interfaces (required for Azure)
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run Streamlit app (replace 'app.py' with your main file if different)
CMD ["streamlit", "run", "interfaz/app/main.py"]