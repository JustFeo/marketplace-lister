# Marketplace Lister

Create items once and publish to multiple marketplaces via adapters.

## Quickstart (dev)

```bash
git clone https://github.com/JustFeo/marketplace-lister.git
cd marketplace-lister
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn src.mlister.main:app --reload
```

OpenAPI: http://localhost:8000/docs

## Docker Compose

```bash
docker compose up -d --build
```

Services: Postgres, Redis, API, Celery worker.

## Core endpoints
- Items CRUD, image upload
- Marketplaces and accounts
- Postings: create, status, retry

## Tests

```bash
pytest -q
```

## License
MIT
