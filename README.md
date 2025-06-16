# [Online BigPen Kenya](https://github.com/tawalabora/bigpen)

A Django-based web application for **Online Bigpen Kenya**.

## ⚙️ Setup Guide

This guide walks you through setting up the project for both **development** and **production** environments.

### A. 📋 Prerequisites

These apply to **both** development and production setups:

- 🐍 Python 3.13 or higher
- 📦 Poetry package manager (Python)
- 📦 NPM package manager (Nodejs)
- 🐘 PostgreSQL (optional - defaults to SQLite for development)

### B. ⚙️ Poetry and NPM Installation

1. Install Poetry using pip:

   ```bash
   pip install poetry
   ```

2. **(Optional)** Configure Poetry to create virtualenv inside project roots.

   ```bash
   poetry config.virtualenvs.in-project true
   ```

3. Install NPM (`npm` comes with **NodeJs** by default when you install it)

4. Install dependencies:

   - For **development** (includes dev tools and test libs):

     ```bash
     poetry install
     ```

   - For **production** (excludes dev dependencies):

     ```bash
     poetry install --only main
     ```

### C. 🛠️ Environment Configuration

Set up a `.env` file in your production environment (You can also setup in your development environment, though not required as defaults will be used):

```bash
# Environment (defaults to 'development')
ENVIRONMENT="production"

# Secret Key (defaults to 'Make sure to set your own secret key!')
SECRET_KEY="your-secure-key-here"

# Allowed Hosts (Defaults to 'localhost,127.0.0.1,dev.tawalabora.space')
ALLOWED_HOSTS="localhost,127.0.0.1,example.com,www.example.com"

# Database Configuration
# SQLite (default - no configuration needed)
# For PostgreSQL, set all the following:
DB_POSTGRESQL=True
DB_NAME=your_database_name
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
# Console email backend (default - no configuration needed)
# For SMTP email backend, set all the following:
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-app-password"

# Custom App Name (defaults to 'apps.custom')
# CUSTOM_APP_NAME=""

# Custom App URL Path Configuration (defaults to 'dashboard/')
# CUSTOM_APP_URL=""
```

### D. 🗄️ Database Setup

#### SQLite (Default - Development)

By default, the system uses SQLite which requires no additional setup.

#### PostgreSQL (Optional - Production Recommended)

If using PostgreSQL:

1. **Install PostgreSQL** on your system
2. **Create a database**:
   ```sql
   CREATE DATABASE your_database_name;
   ```
3. **Configure environment variables** in your `.env` file as shown above

#### Database Migration (Both SQLite and PostgreSQL)

1. Create database tables:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

2. Create the cache table (required for DatabaseCache):

    ```bash
    python manage.py createcachetable
    ```

3. (Optional) Load sample data:

    - 📄 Create a new `fixtures` folder out of the `examples` folder in the `seed` app.
    - 📝 Edit the json files in the created `fixtures` folder tailoring it to your needs.
    - 📤 Load fixtures using:

    ```bash
    python manage.py seed
    ```

**Note**: The `fixtures` folder inside the `apps/seed` directory is gitignored.

### E. 📦 Static Files (Production Only)

If you're deploying to production and using a web server (like Nginx) to serve static files, collect them into a single location using:

   ```bash
   python manage.py buildstatic
   ```

⚠️ This step is not needed in development, as Django serves static files automatically when `DEBUG=True`.

## 🚀 Running the Application

Start the development server:

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`
