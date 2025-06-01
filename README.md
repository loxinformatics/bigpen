![](./app/home/static/home/img/logo.png)

# [Online BigPen Kenya](https://github.com/loxinformatics/bigpen)

## Environment Variables

During development, the `.env` file is optional as the system will use default values as `DEBUG`  settings will be **`True`**. However, if you need to customize any settings, copy these variables into your `.env` and update the values as needed:

```bash
# -------------- Debug setting --------------
# The default is 'True' unless explicitly changed in settings.py
# Ensure DEBUG is 'False' when in production.

DEBUG="False"

# -------------- Secret key setting --------------
# The default is 'Make sure to set your own secret key!'

SECRET_KEY="vdfasW^f34rewdfK3io2r230dbicndori329!3obsx"

# -------------- Allowed hosts setting --------------
# The default is 'localhost,127.0.0.1,dev.tawalabora.space'.
# Ensure you still include 'localhost' and '127.0.0.1' as well, together with your site domain
# when in production.

ALLOWED_HOSTS="localhost,127.0.0.1,example.com,www.example.com"

# -------------- Database settings --------------.
# The default database used is SQLite.
# Below is an example of configuring Postgre.

DB_ENGINE="django.db.backends.postgresql"
DB_USER=""
DB_PASSWORD=""
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME=""

# -------------- Email settings --------------
# The default configuration prints emails to the console / terminal when sent.
# Below is an example of using gmail smtp serve to actually send an email.

EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
EMAIL_HOST="smtp.gmail.com"
```

## Poetry Setup

1. Install Poetry using pip:
```bash
pip install poetry
```

2. (Optional) Configure Poetry to create virtualenv in project directory:
```bash
poetry config virtualenvs.in-project true
```

3. Install project dependencies:
```bash
poetry install
```

This will create a virtual environment and install all dependencies specified in `pyproject.toml`.

## Database Setup

After installing dependencies, set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

(Optional) If you want to populate the database with sample data:

```bash
python manage.py seed
```

This will seed the database with initial fixtures provided with the application.
