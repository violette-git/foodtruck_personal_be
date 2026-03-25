# Not Quite Hawaiian Food Truck (NQHFT)

A Django web application for managing and operating the "Not Quite Hawaiian Food Truck" business. The app provides customer-facing ordering and information pages, a user authentication system, location services, and an admin controller interface.

---

## Features

- **User accounts** — Registration, login, logout, and personal dashboards
- **Menu/display page** — Presents food truck information and offerings
- **Location services** — `/whereami/` redirects customers to Google Maps directions
- **Customer management** — Stores customer profiles with contact info, profile pictures, and coupon counts
- **Admin controller** — Business operations management interface
- **Progressive Web App (PWA)** — Installable on mobile devices

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.0.4 (Python) |
| Database | PostgreSQL (via psycopg2) |
| Frontend | Bootstrap 5.2.0, Swiper.js, Chart.js |
| WSGI Server | Gunicorn |
| Static Files | WhiteNoise |
| Containerization | Docker + docker-compose |
| Deployment | Heroku-ready (Procfile included) |

---

## Project Structure

```
foodtruck_personal_be/
├── foodtruckpersonalbe/     # Django project config (settings, root urls)
├── user_app/                # User authentication app (models, views, urls)
├── foodtruckapp/            # Food truck business logic (models, views, urls)
├── templates/               # HTML templates
│   ├── base.html
│   ├── navbar.html
│   ├── footer.html
│   ├── user_app/            # Login, register, dashboard templates
│   └── foodtruckapp/        # Display, controller, whereami templates
├── static/                  # CSS, JS, fonts, images
├── Dockerfile
├── docker-compose.yml
├── Procfile
└── requirements.txt
```

---

## Data Models

### `User` (user_app)
Extends Django's `AbstractUser` with:
- `username` — Unique, max 23 characters
- `is_a_superuser` — Custom admin access flag

### `Email_List` (foodtruckapp)
Stores customer contact and loyalty info:
- `username` — OneToOne link to User
- `name` — Customer name
- `number` — Phone number
- `profile_pic` — Profile image
- `email` — Email address
- `coupon_count` — Loyalty coupon tally

---

## URL Routes

### User App
| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/register/` | Create a new account |
| `/login/` | Log in |
| `/logout/` | Log out |
| `/dashboard/<username>` | User profile dashboard (login required) |

### Food Truck App
| URL | Description |
|-----|-------------|
| `/display/` | Menu and food truck information |
| `/controller/` | Admin/business operations interface |
| `/whereami/` | Redirects to Google Maps for truck location |

### Admin
| URL | Description |
|-----|-------------|
| `/admin/` | Django admin panel |

---

## Getting Started

### Prerequisites
- Docker and docker-compose

### Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd foodtruck_personal_be
   ```

2. Create a `.env` file (or set environment variables):
   ```env
   POSTGRES_NAME=foodtruck
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=yourpassword
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. The app will be available at `http://localhost:8000`.

> The Docker entrypoint automatically waits for PostgreSQL to be ready and runs migrations before starting the server.

---

## Deployment

The project includes a `Procfile` for Heroku deployment using Gunicorn. The `django-heroku` package handles Heroku-specific configuration automatically.

```bash
heroku create
git push heroku main
heroku run python manage.py migrate
```

---

## Authentication

Session-based authentication using Django's built-in auth system. Protected views use the `@login_required` decorator. The custom `User` model is set as `AUTH_USER_MODEL`.
