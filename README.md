# Project 404 - Backend

This is a Django 5 backend for the Project 404 application, providing RESTful APIs for user authentication, task management, and image annotation.

## Tech Stack
- Django 5
- Django REST Framework (DRF)
- djangorestframework-simplejwt (JWT Authentication)
- django-cors-headers
- django-filter
- Pillow (Image Processing)
- python-decouple (Environment Variables)
- SQLite (Database)

## Setup Instructions

1. Ensure you have Python >= 3.12 installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables:
   Copy `.env.example` to `.env` and configure `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `CORS_ALLOWED_ORIGINS`.
5. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Seed the database with demo tasks:
   ```bash
   python manage.py seed_demo_tasks
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables

- `SECRET_KEY`: Django secret key.
- `DEBUG`: Set to `True` for development.
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts.
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins (e.g., `http://localhost:3000`).
- `ACCESS_TOKEN_LIFETIME_MINUTES`: JWT access token lifetime.
- `REFRESH_TOKEN_LIFETIME_DAYS`: JWT refresh token lifetime.

## Difficulties & Solutions

1. **Custom Error Envelope**: Ensuring every API endpoint returned a standardized `{ success, message, data/errors }` envelope was challenging due to DRF's default exception handling. We solved this by implementing a global exception handler in `apps/common/exceptions.py` that intercepts DRF's exceptions and reformats them.
2. **Email-based Authentication**: Django's default User model requires a username. We solved this by creating a custom `UserManager` and extending `AbstractUser` to remove the `username` field and set `USERNAME_FIELD = "email"`.
