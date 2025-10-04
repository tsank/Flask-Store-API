# Flask Store API

A RESTful API for managing stores, items, and tags using Flask, SQLAlchemy, and Flask-Smorest.

## Features
- Create, list, update, and delete stores
- Create, list, update, and delete items
- Create, list, update, and delete tags
- Link tags to items
- Retrieve all tags for a store, including those linked to its items
- SQLite database support
- Docker and docker-compose setup

## Endpoints
- `/store` : List and create stores
- `/store/<store_id>` : Get or delete a store
- `/store/<store_id>/tag` : List and create tags for a store
- `/item` : List and create items
- `/item/<item_id>` : Get, update, or delete an item
- `/item/<item_id>/tag/<tag_id>` : Link or unlink a tag to an item
- `/tag/<tag_id>` : Get or delete a tag

## Tech Stack
- Python 3.13+
- Flask
- Flask-Smorest
- SQLAlchemy
- Marshmallow
- Docker

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run with Flask: `flask run`
4. Or use Docker: `docker-compose up`

## Usage
Use tools like Insomnia or Postman to interact with the API endpoints. See endpoint documentation above for request/response formats.

## Folder Structure
- `app.py` : Main application factory
- `models/` : SQLAlchemy models
- `resources/` : API endpoint implementations
- `schemas.py` : Marshmallow schemas
- `db.py` : Database setup
- `requirements.txt` : Python dependencies
- `Dockerfile` & `docker-compose.yml` : Container setup

## License
MIT