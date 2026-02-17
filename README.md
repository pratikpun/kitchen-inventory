# Kitchen Inventory

I kept opening my fridge, staring at random ingredients, and closing it again. I'd either cook the same three meals on repeat or let things expire because I couldn't figure out what to make with what I had.

This project is my attempt at solving that. The idea is simple: track what's in your kitchen, and get recipe suggestions based on what you actually have - no grocery run required.

## What I'm building

A full-stack app that:
- Tracks kitchen ingredients and quantities
- Suggests recipes you can cook right now with what's on hand
- Deducts inventory after you cook something
- Categorises meals by type (breakfast/lunch/dinner) and cooking time

## Where things stand

**Backend (in progress)**
- REST API built with FastAPI + SQLAlchemy
- PostgreSQL database for persistence
- Full CRUD for kitchen inventory items (`/items`)
- Health check endpoint
- Tests with pytest

**Frontend** - not started yet

**Recipe engine** - not started yet

## Current API

| Method   | Endpoint         | Description          |
|----------|------------------|----------------------|
| `GET`    | `/health`        | Health check         |
| `GET`    | `/items`         | List all items       |
| `POST`   | `/items`         | Add an item          |
| `GET`    | `/items/{id}`    | Get a single item    |
| `PUT`    | `/items/{id}`    | Update an item       |
| `DELETE` | `/items/{id}`    | Delete an item       |

## Tech stack

- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL
- **Testing:** pytest, httpx
- **Linting:** Ruff + pre-commit hooks
- **Containerisation:** Docker, Docker Compose
- **CI/CD:** GitHub Actions (lint + test on every push)
- **Cloud:** AWS (ECR, ECS Fargate, RDS)

## Running locally

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Requires a local PostgreSQL instance with a `kitchen_inventory` database.

## Running with Docker

```bash
cd backend
docker compose up --build
```

This starts both the API and a PostgreSQL container. Requires a `.env` file (see `.env.example`).

## Running tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

Requires a local `kitchen_inventory_test` database.

## AWS deployment

The backend has been deployed to AWS using:
- **ECR** for Docker image storage
- **ECS Fargate** for running the container (serverless, no servers to manage)
- **RDS** for managed PostgreSQL

Key commands for redeployment:

```bash
# Build for AWS (must target amd64, not ARM)
docker build --platform linux/amd64 -t kitchen-inventory .

# Tag and push to ECR
docker tag kitchen-inventory:latest <account-id>.dkr.ecr.eu-west-2.amazonaws.com/kitchen-inventory:latest
docker push <account-id>.dkr.ecr.eu-west-2.amazonaws.com/kitchen-inventory:latest

# Force ECS to pick up the new image
aws ecs update-service --cluster kitchen-inventory --service kitchen-inventory-service --force-new-deployment --region eu-west-2
```

## What's next

- Recipe and recipe-ingredient models
- Recipe matching engine (what can I cook with what I have?)
- Inventory deduction on cook events
- Frontend (likely React or Next.js)

## Approach

I'm treating this as an end-to-end ownership exercise - product thinking, system design, API design, testing, deployment - not just writing code. Building it incrementally, making decisions along the way, and documenting the tradeoffs as I go.
