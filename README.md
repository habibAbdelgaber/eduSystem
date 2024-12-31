Django Custom Authentication System with Social Authentication
This project is a fully functional, production-ready Django authentication system featuring custom authentication and Google OAuth2-based social authentication. It is designed to be easily extendable for any Django-based project. It comes pre-configured with GitHub Actions, Docker, and CircleCI for smooth deployment and continuous integration.

Features
Custom user authentication system
Social authentication using Google OAuth2
Fully configured CI/CD pipelines
GitHub Actions for automated testing and deployment
CircleCI for additional CI/CD workflows
Docker support for easy containerized deployment
Open source and extendable for any Django project
Compatibility with major hosting platforms
Getting Started
Prerequisites
Python 3.9+
Docker (optional for containerized deployment)
Git
Django
Google API credentials for OAuth2
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Set up a virtual environment and install dependencies:

bash
Copy code
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
If you are using Poetry for dependency management:

bash
Copy code
poetry install
Apply migrations:

bash
Copy code
python manage.py migrate
Set up .env file:

Create a .env file in the project root with the following environment variables:

env
Copy code
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost, 127.0.0.1
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_client_id
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_client_secret
Run the development server:

bash
Copy code
python manage.py runserver
The application should now be accessible at http://127.0.0.1:8000.

Using Docker
Build the Docker image:

bash
Copy code
docker build -t django-auth-system .
Run the container:

bash
Copy code
docker run -p 8000:8000 django-auth-system
The app will be accessible at http://127.0.0.1:8000.

Configuring Google OAuth2
Go to the Google Cloud Console.
Create a new project and configure the OAuth consent screen.
Under "Credentials," create a new OAuth 2.0 client ID.
Set the redirect URI to http://127.0.0.1:8000/accounts/google/login/callback/.
Copy the client ID and client secret into your .env file.
Running Tests
To run the test suite:

bash
Copy code
python manage.py test
If you are using Docker:

bash
Copy code
docker-compose run app python manage.py test
Deployment
This project supports deployment to most hosting platforms. The configured CI/CD pipelines automate testing and deployment. Follow these general steps:

Push to GitHub: The GitHub Actions workflow is pre-configured to run tests and build Docker images on every push.

CircleCI Integration: Ensure that your CircleCI configuration matches your hosting platform.

Deploy to your preferred hosting platform.

Contributing
Fork the repository.
Create your feature branch: git checkout -b feature/YourFeature.
Commit your changes: git commit -m 'Add YourFeature'.
Push to the branch: git push origin feature/YourFeature.
Open a pull request.
License
This project is licensed under the Apache 2.0 License. Feel free to use, modify, and distribute it for personal and commercial purposes.

Acknowledgments
Django Framework
Google APIs

![Build Status](https://github.com/habibAbdelgaber/eduSystem/actions/workflows/ci.yml/badge.svg)
[![CircleCI](https://circleci.com/gh/habibAbdelgaber/eduSystem/tree/main.svg?style=svg)](https://circleci.com/gh/habibAbdelgaber/eduSystem/tree/main)



