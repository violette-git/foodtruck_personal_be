# CLAUDE.md — AI Assistant Guide for foodtruck_personal_be

This file provides context for AI assistants (Claude, Copilot, etc.) working on this repository.

---

## Project Overview

**Not Quite Hawaiian Food Truck (NQHFT)** — a Django-based backend for a small food truck business. It handles customer registration, authentication, menu display, location services, an admin controller interface, and a basic customer loyalty/coupon system. It is also configured as a Progressive Web App (PWA).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Framework | Django 4.0.4 |
| Database | PostgreSQL (production) / SQLite3 (local fallback) |
| Frontend | HTML5, Bootstrap 5.2.0, Swiper.js, Chart.js |
| Static Files | WhiteNoise 6.2.0 |
| WSGI Server | Gunicorn 20.1.0 |
| Containerization | Docker + docker-compose |
| Deployment Target | Heroku |

---

## Repository Structure

```
foodtruck_personal_be/
├── foodtruckpersonalbe/       # Django project configuration
│   ├── settings.py            # Main settings (DB, auth, static, CORS)
│   ├── urls.py                # Root URL dispatcher
│   ├── wsgi.py / asgi.py      # WSGI/ASGI entry points
├── user_app/                  # Authentication & user management app
│   ├── models.py              # Custom User model (extends AbstractUser)
│   ├── views.py               # register, login, logout, profile views
│   ├── urls.py                # /register/, /login/, /logout/, /dashboard/<username>
│   └── migrations/
├── foodtruckapp/              # Core business logic app
│   ├── models.py              # Email_List customer model
│   ├── views.py               # display, controller, whereami views
│   ├── urls.py                # /display/, /controller/, /whereami/
│   └── migrations/
├── templates/                 # Django HTML templates
│   ├── base.html              # Base layout (Bootstrap, Swiper, fonts)
│   ├── navbar.html            # Navigation with embedded SVG logo
│   ├── footer.html            # Footer with auth links
│   ├── user_app/              # register.html, login.html, mem-dashboard.html
│   └── foodtruckapp/          # display.html, controller.html, whereami.html
├── static/
│   ├── css/styles.css         # Custom styles and font-face declarations
│   ├── js/charts.js           # Chart.js usage
│   └── images/                # Logos, SVGs, font files (.ttf)
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Procfile                   # Heroku: gunicorn foodtruckpersonalbe.wsgi
├── app.manifest               # PWA manifest
└── .env.example               # Environment variable template
```

---

## Data Models

### `user_app.User` (extends `AbstractUser`)
- `username` — CharField, max_length=23, unique
- `is_a_superuser` — BooleanField, default=False (custom admin flag, separate from Django's `is_superuser`)
- Inherits all standard AbstractUser fields

### `foodtruckapp.Email_List` (customer profile)
- `username` — OneToOneField → User (on_delete=CASCADE, related_name='user')
- `name` — CharField(max_length=50)
- `number` — CharField(max_length=20) — phone number
- `profile_pic` — ImageField(upload_to='profile_pics/', blank=True, null=True)
- `email` — EmailField
- `coupon_count` — IntegerField(default=0) — loyalty tracking

**Key relationship:** Every registered User may have one `Email_List` entry representing their customer profile.

---

## URL Routes

| URL Pattern | View | Purpose |
|---|---|---|
| `/` | `user_app.views.base` | Home page |
| `/register/` | `user_app.views.register` | Registration (GET + POST) |
| `/login/` | `user_app.views.login` | Login (GET + POST) |
| `/logout/` | `user_app.views.logout` | Logout, redirects home |
| `/dashboard/<username>` | `user_app.views.profile` | User dashboard (@login_required) |
| `/display/` | `foodtruckapp.views.display` | Menu/food truck display |
| `/controller/` | `foodtruckapp.views.controller` | Admin interface |
| `/whereami/` | `foodtruckapp.views.whereami` | Redirects to Google Maps |
| `/admin/` | Django admin | Django admin panel |

---

## Development Workflows

### Local Setup (without Docker)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables (copy and edit)
cp .env.example .env

# 4. Run migrations (SQLite3 used automatically if POSTGRES_NAME is not set)
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Start dev server
python manage.py runserver
```

### Local Setup (Docker)

```bash
docker-compose up --build
```

The Docker entrypoint automatically:
1. Waits for PostgreSQL on port 5432
2. Runs `makemigrations` and `migrate`
3. Starts `runserver` on `0.0.0.0:8000`

### Common Management Commands

```bash
python manage.py migrate              # Apply migrations
python manage.py makemigrations       # Generate new migrations after model changes
python manage.py test                 # Run tests (test files are currently empty)
python manage.py collectstatic        # Gather static files for production
python manage.py createsuperuser      # Create Django admin user
```

---

## Environment Variables

Defined in `.env.example` and loaded via `python-decouple`:

| Variable | Purpose | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | Hardcoded fallback (insecure) |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `*` |
| `POSTGRES_NAME` | PostgreSQL database name | — (SQLite3 used if absent) |
| `POSTGRES_USER` | PostgreSQL user | — |
| `POSTGRES_PASSWORD` | PostgreSQL password | — |
| `POSTGRES_HOST` | PostgreSQL host | `db` (Docker service name) |

**Production requirements:** Always set `SECRET_KEY`, `DEBUG=False`, and explicit `ALLOWED_HOSTS`.

---

## Database Configuration

- If `POSTGRES_NAME` is set in the environment, Django connects to PostgreSQL.
- Otherwise it falls back to SQLite3 (`db.sqlite3`) — suitable for local development only.
- PostgreSQL host defaults to `db` (Docker Compose service name); override with `POSTGRES_HOST`.

After any model change:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Authentication System

- Custom User model: `AUTH_USER_MODEL = 'user_app.User'`
- Session-based authentication (Django's built-in `django.contrib.auth`)
- Login required decorator used on the `/dashboard/<username>` route
- `is_a_superuser` is a custom BooleanField distinct from Django's `is_superuser`; use this field for app-level admin checks
- Registration view handles `IntegrityError` for duplicate usernames

---

## Frontend Conventions

- Templates extend `templates/base.html` — Bootstrap 5.2.0, Swiper.js, and custom fonts are included there
- Custom fonts (loaded via `@font-face` in `styles.css`): Hawaiian Dreams, Indie Flower, Bebas Neue, Dosis, Cairo, Varela Round — font `.ttf` files live in `static/css/`
- `navbar.html` contains a large embedded SVG logo — do not remove or refactor this inline SVG without designer review
- `Chart.js` is available on all pages via `base.html`; usage is in `static/js/charts.js`
- Media uploads go to `{BASE_DIR}/media/profile_pics/`

---

## Deployment

### Heroku

```bash
heroku create
git push heroku main
heroku run python manage.py migrate
heroku config:set SECRET_KEY=... DEBUG=False ALLOWED_HOSTS=<your-app>.herokuapp.com
```

`django-heroku` is installed and auto-configures `DATABASES`, `STATIC_ROOT`, `ALLOWED_HOSTS`, and logging for the Heroku environment.

### Static Files

WhiteNoise (`whitenoise.storage.CompressedStaticFilesStorage`) serves and compresses static files without a CDN. Run `collectstatic` before deploying.

---

## Known Issues / Security Notes

- `SECRET_KEY` has an insecure hardcoded fallback in `settings.py` — always override via environment variable in any non-local environment.
- `ALLOWED_HOSTS` defaults to `'*'` — restrict this in staging/production.
- `DEBUG` defaults to `True` — set `DEBUG=False` in production.
- `app.manifest` contains a hardcoded local IP (`192.168.68.105`) as `start_url` — update before any real deployment.
- CORS headers package is installed (`django-cors-headers`) but `CORS_ALLOWED_ORIGINS` is not explicitly configured in settings; review before exposing an API.

---

## Testing

Test files exist but are currently empty:
- `user_app/tests.py`
- `foodtruckapp/tests.py`

Run the test suite with:
```bash
python manage.py test
```

When adding tests, use Django's `TestCase` (already imported in both files). Focus on view logic, model validation, and authentication flows first.

---

## Key Conventions for AI Assistants

1. **Model changes always need migrations.** After editing any `models.py`, run `makemigrations` and `migrate`. Never edit migration files directly unless fixing a specific migration issue.
2. **Use the custom User model.** Always reference `from django.contrib.auth import get_user_model; User = get_user_model()` rather than importing `django.contrib.auth.models.User` directly.
3. **`is_a_superuser` vs `is_superuser`.** App-level privilege checks should use `user.is_a_superuser`; `is_superuser` is for Django admin access.
4. **Template inheritance.** All new templates should extend `base.html` and use the `{% block %}` system already in place.
5. **Static files.** New static assets belong in `static/css/`, `static/js/`, or `static/images/`. Reference them with `{% load static %}` and `{% static '...' %}`.
6. **Environment variables.** Never hardcode secrets or credentials. Use `python-decouple`'s `config()` in settings, and add new variables to `.env.example`.
7. **No tests yet.** When implementing new features, add corresponding tests to the appropriate `tests.py` file.
8. **Docker service name.** The PostgreSQL service in docker-compose is named `db`; this is the default `POSTGRES_HOST`.
