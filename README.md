# [Online BigPen Kenya](https://github.com/tawalabora/bigpen)

A Django-based web application for **Online Bigpen Kenya**.

<!-- ## Features
- Feature 1
- Feature 2
- [Add your key features here] -->

## Development Setup

### Prerequisites
- Python 3.13 or higher
- Poetry package manager

### Environment Configuration

The `.env` file is optional during development. Default values will be used if not specified.

```bash
# Development Defaults (ENVIRONMENT=development)
ENVIRONMENT="development"
SECRET_KEY="development-key"
ALLOWED_HOSTS="localhost,127.0.0.1"

# Production Settings Example
ENVIRONMENT="production"
SECRET_KEY="your-secure-key-here"
ALLOWED_HOSTS="localhost,127.0.0.1,example.com,www.example.com"

# Database Configuration (defaults to SQLite)
DB_ENGINE="django.db.backends.postgresql"
DB_NAME="mydb"
DB_USER="myuser"
DB_PASSWORD="mypassword"
DB_HOST="localhost"
DB_PORT="5432"

# Email Configuration (defaults to console backend)
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-app-password"
```

### Poetry Installation

1. Install Poetry using pip:
```bash
pip install poetry
```

2. (Optional) Configure Poetry to create virtualenv in project directory:
```bash
poetry config virtualenvs.in-project true
```

3. Install dependencies based on your `ENVIRONMENT`:
   - For `development` (includes dev tools like django-browser-reload):
   ```bash
   poetry install
   ```
   - For `production` (only main dependencies):
   ```bash
   poetry install --only main
   ```

### Database Setup

1. Create database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. (Optional) Load sample data:
   - Copy `seed_example.json` from any app's fixtures directory
   - Create your own fixture file based on the example
   - Load fixtures using:
   ```bash
   python manage.py seed
   ```

**Note**: Only `seed_example.json` files are tracked in Git. All other fixture files are gitignored.

## Production Deployment
- Set `ENVIRONMENT="production"` in your environment
- Configure a secure `SECRET_KEY`
- Set appropriate `ALLOWED_HOSTS`
- Install only main dependencies: `poetry install --only main`
