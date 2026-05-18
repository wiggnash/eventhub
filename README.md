# EventHub

A backend API for a simplified event ticketing platform built with Django and Django REST Framework.

## Overview

EventHub allows users to browse events, reserve seats, and cancel reservations. The platform handles concurrent seat booking scenarios to ensure seat availability is managed accurately even when multiple users attempt to book the last seat simultaneously.

## Features

- Browse available events
- Reserve seats for an event
- Cancel existing reservations
- Race condition-safe seat availability management

## Tech Stack

- **Python** 3.12+
- **Django** — ORM, models, database queries
- **Django REST Framework** — serializers, ViewSets, Routers
- **SQLite** (development) — swappable for PostgreSQL in production

## Project Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/) installed on your system

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd eventhub

# Install dependencies and create virtual environment
uv sync

# Run database migrations
uv run manage.py migrate

# Start the development server
uv run manage.py runserver
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/events/` | List all events |
| GET | `/api/events/{id}/` | Retrieve a single event |
| POST | `/api/reservations/` | Reserve a seat |
| DELETE | `/api/reservations/{id}/` | Cancel a reservation |

> Endpoints will be updated as the project evolves.

## Environment Variables

Copy `.env.example` to `.env` and fill in the values before running the project.

```bash
cp .env.example .env
```
