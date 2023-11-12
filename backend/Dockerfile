# Pull base image
FROM python:3.12

# Set working directory
WORKDIR /backend

# Copy project into container
COPY . /backend

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run app.py when container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]