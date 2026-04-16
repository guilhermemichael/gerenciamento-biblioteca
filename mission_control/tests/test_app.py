import os
import tempfile

import pytest
from app import create_app
from app.database import db


def test_create_app():
    app = create_app()
    assert app is not None
    assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    app = create_app()
    app.testing = True

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_create_author(client):
    response = client.post(
        "/api/v1/authors",
        json={"name": "Isaac Asimov"},
    )
    assert response.status_code == 201
    assert response.json["name"] == "Isaac Asimov"


def test_list_authors(client):
    client.post("/api/v1/authors", json={"name": "Ursula K. Le Guin"})
    response = client.get("/api/v1/authors")
    assert response.status_code == 200
    assert any(author["name"] == "Ursula K. Le Guin" for author in response.json)
