# Gloryphonics API

Production backend for the Gloryphonics music platform, built with Django and Django REST Framework.

## Overview

Gloryphonics API powers user management, bands, media, comments, and donations. It is designed to run in production behind Nginx with TLS certificates managed by Certbot.

## Key Features

- User registration and account management
- JWT authentication (access and refresh tokens)
- Band management endpoints
- Band images and comments
- PayPal donation flow and webhook handling
- OpenAPI schema with Swagger and ReDoc

## Tech Stack

- Python 3
- Django 5
- Django REST Framework
- Simple JWT
- drf-spectacular
- PostgreSQL
- AWS S3 (media storage)
- Docker & Docker Compose
- Nginx + Certbot

## Project Structure

```text
.
├── band/                 # Bands, images, comments
├── user/                 # Users and account flows
├── payment/              # Donations and PayPal webhook
├── gloryphonics/         # Django settings and root URLs
├── docker-compose.yml    # web / nginx / certbot services
├── Dockerfile
└── manage.py
```

## Production Environment Variables

Create a `.env` file and provide the required values:

```env
DJANGO_SECRET_KEY=your-secret-key

# Database (PostgreSQL)
PG_NAME=gloryphonics
PG_USER=postgres
PG_PASSWORD=postgres
PG_HOST=postgres
PG_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=app-password

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
```

## Production Run (Docker Compose)

```bash
docker compose up --build -d
```

Services defined in `docker-compose.yml`:

- `web`: Django application container
- `nginx`: Reverse proxy and static files
- `certbot`: TLS certificate management

## API Documentation

After deployment:

- OpenAPI schema: `/api/doc/`
- Swagger UI: `/api/doc/swagger/`
- ReDoc: `/api/doc/redoc/`

## Authentication Endpoints

- `POST /api/token/` — obtain JWT pair
- `POST /api/token/refresh/` — refresh access token

## Main Route Prefixes

- `/api/users/`
- `/api/bands/`
- `/api/payments/`

## Deployment Notes

- The project is configured for HTTPS behind a proxy (`SECURE_PROXY_SSL_HEADER`).
- Trusted origins should match your production domains.
- Media files are stored in AWS S3.
