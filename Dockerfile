# using an official Python runtime as a parent image
FROM python:3.9-slim
# Setting Environment Variables
ENV PYTHONDONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Setting the working directory
WORKDIR / app

# Install System Dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    curl
# Installing dependencies
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copying project
COPY . /app/

# Collecting Static files
RUN python manage.py collectstatic --noinput

# Run Migrations
RUN python manage.py migrate

# expose port 8000
EXPOSE 8000

# Running the Django development server (using gunicorn or wsgi for production)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_project.wsgi:application"]
