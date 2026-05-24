# EventHub

A backend API for a simplified event ticketing platform built with Django and Django REST Framework.

## Overview

EventHub allows users to register, log in, browse events, reserve seats, and cancel reservations. JWT authentication protects all write operations, and seat availability is validated at the serializer level to prevent overbooking.

## Tech Stack

- **Python** 3.12+
- **Django** — ORM, models, middleware
- **Django REST Framework** — serializers, ViewSets, SimpleRouter
- **SimpleJWT** — JWT-based authentication
- **SQLite** (development) — swappable for PostgreSQL in production
- **uv** — package and environment management

## Project Structure

```
eventhub/
├── eventhub/           # Project config (settings, urls, middleware)
├── events/             # Event model, ViewSet, serializer
├── profiles/           # User registration, login, profile model
├── reservations/       # Reservation model, ViewSet, serializer
└── manage.py
```

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/) installed on your system

### Installation

```bash
git clone <repo-url>
cd eventhub

# Install dependencies
uv sync

# Apply migrations
uv run manage.py migrate

# Create a superuser (optional)
uv run manage.py createsuperuser

# Start the development server
uv run manage.py runserver
```

## Authentication

This project uses JWT (JSON Web Tokens) via `djangorestframework-simplejwt`.

### Register

```
POST /api/profiles/register/
```

**Payload:**
```json
{
    "username": "john",
    "email": "john@example.com",
    "password": "securepassword",
    "bio": "Event enthusiast",
    "phone": "9876543210"
}
```

**Response:**
```json
{
    "user_id": 1,
    "profile_id": 1,
    "username": "john",
    "email": "john@example.com"
}
```

### Login

```
POST /api/profiles/login/
```

**Payload:**
```json
{
    "username": "john",
    "password": "securepassword"
}
```

**Response:**
```json
{
    "user_id": 1,
    "username": "john",
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

### Using the Token

Pass the access token in the `Authorization` header for all protected endpoints:

```
Authorization: Bearer <access_token>
```

### Refresh Token

```
POST /api/token/refresh/
```

```json
{
    "refresh": "<refresh_token>"
}
```

## API Endpoints

### Events

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/events/` | List all events |
| GET | `/api/events/?status=upcoming` | Filter events by status |
| GET | `/api/events/?venue=chennai` | Filter events by venue (case-insensitive) |
| GET | `/api/events/{id}/` | Retrieve a single event |
| POST | `/api/events/` | Create an event |
| PUT | `/api/events/{id}/` | Update an event |
| PATCH | `/api/events/{id}/` | Partially update an event |
| DELETE | `/api/events/{id}/` | Delete an event |

**Create/Update payload:**
```json
{
    "title": "Tech Meetup Chennai",
    "venue": "IIT Madras Research Park",
    "date": "2026-06-15",
    "total_seats": 100,
    "available_seats": 100,
    "status": "upcoming"
}
```

> `created_by`, `updated_by`, `created_at`, `updated_at` are set automatically — do not include in the payload.

**Response includes computed field:**
```json
{
    "id": 1,
    "title": "Tech Meetup Chennai",
    "venue": "IIT Madras Research Park",
    "date": "2026-06-15",
    "total_seats": 100,
    "available_seats": 100,
    "status": "upcoming",
    "reservations_count": 3
}
```

**Status choices:** `upcoming` | `ongoing` | `completed` | `cancelled`

---

### Reservations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reservations/` | List all reservations |
| GET | `/api/reservations/?event_id=1` | Filter reservations by event |
| GET | `/api/reservations/{id}/` | Retrieve a single reservation |
| POST | `/api/reservations/` | Create a reservation |
| POST | `/api/reservations/{id}/cancel/` | Cancel a reservation |

**Create payload:**
```json
{
    "event": 1,
    "profile": 1,
    "seats_reserved": 2
}
```

> Reserving seats automatically decrements `available_seats` on the event.
> Cancelling a reservation automatically restores `available_seats` on the event.

**Validation rules:**
- `seats_reserved` must be at least 1
- Cannot reserve seats for a `completed` or `cancelled` event
- Cannot reserve more seats than `available_seats` on the event

**Status choices:** `confirmed` | `cancelled`

---

## Middleware

`RequestLoggingMiddleware` logs every request with method, path, response status code, and duration:

```
INFO GET /api/events/ - 200 - 0.03s
```

## Models

### Event
| Field | Type | Notes |
|-------|------|-------|
| `title` | CharField | |
| `venue` | CharField | |
| `date` | DateField | |
| `total_seats` | PositiveIntegerField | |
| `available_seats` | PositiveIntegerField | Must not exceed `total_seats` |
| `status` | CharField | choices: upcoming, ongoing, completed, cancelled |
| `created_at` | DateTimeField | auto set on create |
| `updated_at` | DateTimeField | auto set on every save |
| `created_by` | FK → User | auto set from request |
| `updated_by` | FK → User | auto set from request |

### Profile
| Field | Type | Notes |
|-------|------|-------|
| `user` | OneToOneField → User | |
| `bio` | TextField | optional |
| `phone` | CharField | optional |
| `created_at` | DateTimeField | auto set on create |
| `updated_at` | DateTimeField | auto set on every save |

### Reservation
| Field | Type | Notes |
|-------|------|-------|
| `event` | FK → Event | |
| `profile` | FK → Profile | |
| `seats_reserved` | PositiveIntegerField | minimum 1 |
| `status` | CharField | choices: confirmed, cancelled |
| `created_at` | DateTimeField | auto set on create |
| `updated_at` | DateTimeField | auto set on every save |
| `created_by` | FK → User | auto set from request |
| `updated_by` | FK → User | auto set from request |
