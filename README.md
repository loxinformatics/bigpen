![](base/assets/base/img/logo.png)

# prototype

## Environment Variables

Below is the configuration required for the application. Copy these variables into your `.env` and update the values as needed:

```bash
# App settings
SECRET_KEY="Make sure to change this!"
DEBUG="True"
ALLOWED_HOSTS="localhost,127.0.0.1,dev1.treeolive.tech"

# Company details
COMPANY_FULLNAME=""
COMPANY_SHORTNAME=""
COMPANY_MOTTO=""
COMPANY_ACCENT_COLOR=""

# Database settings (DEBUG is False)
DB_ENGINE="django.db.backends.postgresql"
DB_USER=""
DB_PASSWORD=""
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME=""

# Email settings  (DEBUG is False)
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
EMAIL_HOST="smtp.gmail.com"

```
