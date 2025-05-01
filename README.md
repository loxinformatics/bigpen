![](base/assets/base/img/logo.png)

# prototype

## Environment Variables

Below is the configuration required for the application. Copy these variables into your `.env` and update the values as needed:

```bash
# Secret key
SECRET_KEY="Make sure to set your own secret key!"

# Debug: Ensure DEBUG is 'False' when in production. The default is 'True' unless explicitly changed in settings.py
DEBUG=""

# Allowed hosts
ALLOWED_HOSTS="localhost,127.0.0.1,example.com,www.example.com"

# Organization settings
ORG_FULLNAME=""
ORG_SHORTNAME=""
ORG_MOTTO=""
ORG_ACCENT_COLOR=""

# Database settings: Only applies when DEBUG is 'False' unless explicitly changed in settings.py
DB_ENGINE="django.db.backends.postgresql"
DB_USER=""
DB_PASSWORD=""
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME=""

# Email settings: Only applies when DEBUG is 'False' unless explicitly changed in settings.py
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
EMAIL_HOST="smtp.gmail.com"

```
