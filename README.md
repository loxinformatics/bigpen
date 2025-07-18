# Django Template App.

This guide walks you through setting up the project for a **development** environment.

## A. 📋 Prerequisites

- 📦 Poetry package manager (Python)
- 📦 NPM package manager (Nodejs)

By default, SQLite3 is the database system employed. But you can use other DBMSs such as PostgreSQL.

## B. 🔧 Configuration Variables

Set these in your `.env` file as needed. Defaults are preconfigured for development.

---

### 🧠 Core Django Settings

| Variable               | What it's for                         | Default Value                                      |
|------------------------|---------------------------------------|----------------------------------------------------|
| DJANGO_SETTINGS_MODULE | Django settings module to use         | `settings.core.main`                                    |
| ROOT_URLCONF           | Django root URL configuration module  | `settings.core.urls`                                        |
| ENVIRONMENT            | Set to `"production"` for production  | `development`                                      |
| SECRET_KEY             | Django secret key                     | `Make sure to set your own secret key!`            |
| ALLOWED_HOSTS          | Comma-separated list of allowed hosts | `localhost,127.0.0.1` |

---

### 🗄️ Database Configuration

| Variable     | What it's for                        | Default Value |
|--------------|--------------------------------------|---------------|
| DB_BACKEND   | Database backend engine              | `sqlite3`     |
| DB_NAME      | Database name (PostgreSQL only)      | _(none)_      |
| DB_USER      | Database user (PostgreSQL only)      | `postgres`    |
| DB_PASSWORD  | Database password (PostgreSQL only)  | `postgres`    |
| DB_HOST      | Database host (PostgreSQL only)      | `localhost`   |
| DB_PORT      | Database port (PostgreSQL only)      | `5432`        |

---

### 📧 Email Configuration

| Variable            | What it's for             | Default Value                                        |
|---------------------|---------------------------|------------------------------------------------------|
| EMAIL_BACKEND       | Django email backend      | `django.core.mail.backends.console.EmailBackend`     |
| EMAIL_HOST          | SMTP server host          | _(none)_                                             |
| EMAIL_HOST_USER     | SMTP username             | _(none)_                                             |
| EMAIL_HOST_PASSWORD | SMTP password             | _(none)_                                             |

---

### 🌐 Site Configuration

| Variable                 | What it's for                        | Default Value                                    |
|--------------------------|--------------------------------------|--------------------------------------------------|
| SITE_URL                 | Public-facing site URL               | `https://preview.bigpen.co.ke`                  |
| SITE_NAME                | Full name of the site                | `Online BigPen Kenya`                            |
| SITE_SHORT_NAME          | Short name / branding                | `BigPen`                                         |
| SITE_DESCRIPTION         | Site meta description                | `Delivering Stationery Supplies`                |
| SITE_THEME_COLOR         | Theme color for browser UI           | `#ef4444`                                        |
| SITE_KEYWORDS            | Comma-separated SEO keywords         | `bigpen,Online BigPen Kenya,ecommerce`           |
| SITE_AUTHOR              | Site author metadata                 | `christianwhocodes`                              |
| SITE_AUTHOR_URL          | URL to author profile                | `https://github.com/christianwhocodes/`         |
| SITE_NAVIGATION_TYPE          | Type of navigation - `navbar` or `sidebar`               | `navbar`         |

---

### 🖼️ Site Assets

| Variable                 | What it's for                        | Default Value                                      |
|--------------------------|--------------------------------------|----------------------------------------------------|
| SITE_LOGO                | Path to logo image                   | `/lib/static/core/img/logo.png`                   |
| SITE_FAVICON             | Path to favicon icon                 | `/lib/static/core/img/favicon.ico`                |
| SITE_APPLE_TOUCH_ICON    | Apple-specific icon                  | `/lib/static/core/img/apple-touch-icon.png`       |
| SITE_ANDROID_CHROME_ICON | Android Chrome-specific icon         | `/lib/static/core/img/android-chrome-icon.png`    |
| SITE_MSTILE              | Microsoft tile icon                  | `/lib/static/core/img/mstile.png`                 |
| SITE_HERO                | Hero/banner image                    | `/lib/static/core/img/hero.jpg`                   |
| SITE_MANIFEST            | Web manifest path                    | `/lib/static/core/manifest.webmanifest`           |

---