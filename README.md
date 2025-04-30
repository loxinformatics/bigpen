![](base/assets/base/img/logo.png)

# prototype

## Environment Variables

Below is the configuration required for the application. Copy these variables into your `.env` and update the values as needed:

```bash
### ------------- Required -------------

# App settings
SECRET_KEY="Make sure to change this!"
DEBUG="True"
ALLOWED_HOSTS="localhost,127.0.0.1,dev1.treeolive.tech"

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

# Application settings
NEXT_PUBLIC_APP_FULLNAME="Online BigPen Kenya"
NEXT_PUBLIC_APP_SHORTNAME="BigPen"
NEXT_PUBLIC_APP_DESCRIPTION="Your app description"

# Theme settings
NEXT_PUBLIC_PRIMARY_COLOR="red"
```
