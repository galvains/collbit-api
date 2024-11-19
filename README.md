# COLLBIT API

API for working with p2p transactions. User authorization with JWT token is implemented.

## Features

**Ticket:**
    * GET, POST, DELETE methods have been implemented.
    * ticket filtering has been implemented.

**Subscription**
    * Subscription system implemented.

**User**
    * The system of role distribution (admin, staff, regular user) is implemented.
    * Authorization with JWT token.

## Stack

**Backend:** Python, FastApi, Swagger
**DB:** PostgreSQL
**Other:** Docker-Compose

## Setup and run

**Clone repo:**
   
```bash
git clone https://github.com/galvains/collbit-api.git
```
**Dependencies:**
   
```bash
pip install -r /src/requirements.txt
```

**Run:**

```bash
docker compose -f docker-compose.dev.yml up
```
