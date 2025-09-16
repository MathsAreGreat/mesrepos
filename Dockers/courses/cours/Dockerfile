ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# Set the working directory
WORKDIR /app/cours

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Flask app code and templates
COPY app.py app.py
COPY templates/ templates/
COPY . .

# Expose port 7000
EXPOSE 7000

# Run the application
CMD ["python", "app.py"]
