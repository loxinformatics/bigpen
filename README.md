# Ecommerce Django App.

This guide walks you through setting up the project for a **development** environment.

## A. 📋 Prerequisites

- 📦 Poetry package manager (Python)
- 📦 NPM package manager (Nodejs)

By default, SQLite3 is the database system employed. But you can use other DBMSs such as PostgreSQL.

## B. 🛠️ Environment Configuration

Set up a `.env` file only if you need to override variables.
For example if you are using another database management system such as PostgreSQL besides SQLite.
Or if you want to test out a mail server _(By default, emails sent are simply printed out in the terminal / console)_.
Below is a table of supported environment variables:

| Variable            | What it's for                         | Default Value                                      |
| ------------------- | ------------------------------------- | -------------------------------------------------- |
| ENVIRONMENT         | Set to `"production"` for production  | `development`                                      |
| SECRET_KEY          | Django secret key                     | `Make sure to set your own secret key!`            |
| ALLOWED_HOSTS       | Comma-separated list of allowed hosts | `localhost,127.0.0.1,8000.christianwhocodes.space` |
| DB_BACKEND          | Database backend engine               | `sqlite3`                                          |
| DB_NAME             | Database name (PostgreSQL only)       | _(none)_                                           |
| DB_USER             | Database user (PostgreSQL only)       | `postgres`                                         |
| DB_PASSWORD         | Database password (PostgreSQL only)   | `postgres`                                         |
| DB_HOST             | Database host (PostgreSQL only)       | `localhost`                                        |
| DB_PORT             | Database port (PostgreSQL only)       | `5432`                                             |
| EMAIL_BACKEND       | Django email backend                  | `django.core.mail.backends.console.EmailBackend`   |
| EMAIL_HOST          | SMTP server host                      | _(none)_                                           |
| EMAIL_HOST_USER     | SMTP username                         | _(none)_                                           |
| EMAIL_HOST_PASSWORD | SMTP password                         | _(none)_                                           |
| SITE_APP            | Django custom app name                | `apps.default`                                     |

## C. ⚙️ Setup Commands

1. **(Optional)** Configure Poetry to create virtualenv inside project roots.

   ```bash
   poetry config.virtualenvs.in-project true
   ```

2. Install dependencies

   ```bash
     poetry install
     poetry run python manage.py npm install
   ```

3. Create database tables:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```


## D. 🚀 Running the Application

Start the development server:

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`
