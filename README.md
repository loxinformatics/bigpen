![](./app/home/static/home/img/logo.png)

# Online BigPen Kenya

## Environment Variables

Below is the configuration required for the application. Copy these variables into your `.env` and update the values as needed:

```bash
# -------------- Debug setting --------------
# The default is 'True' unless explicitly changed in settings.py
# Ensure DEBUG is 'False' when in production.

# DEBUG="False"

# -------------- Secret key setting --------------
# The default is 'Make sure to set your own secret key!'

# SECRET_KEY="vdfasW^f34rewdfK3io2r230dbicndori329!3obsx"

# -------------- Allowed hosts setting --------------
# The default is 'localhost,127.0.0.1,dev.treeolive.tech'.
# Ensure you still include 'localhost' and '127.0.0.1' as well, together with your site domain
# when in production.

# ALLOWED_HOSTS="localhost,127.0.0.1,example.com,www.example.com"

# -------------- Database settings --------------
# When DEBUG is 'True' it uses a sqlite database with a file named `db.sqlite3`.
# The below settings only apply when DEBUG is 'False' unless explicitly changed in `settings.py`.

# DB_ENGINE="django.db.backends.postgresql"
# DB_USER=""
# DB_PASSWORD=""
# DB_HOST="localhost"
# DB_PORT="5432"
# DB_NAME=""

# -------------- Email settings --------------
# When DEBUG is 'True' it uses the console as an email backend
# therefore any email sent is printed out in the console / terminal.
# The below settings only apply when DEBUG is 'False' unless explicitly changed in settings.py.

# EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST_USER=""
# EMAIL_HOST_PASSWORD=""
# EMAIL_HOST="smtp.gmail.com"

```
