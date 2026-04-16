from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from ..database import db
from ..models.author import Author
from ..models.book import Book
from ..schemas.library_schema import AuthorSchema, BookSchema

api_v1 = Blueprint("api_v1", __name__)


@api_v1.route("/authors", methods=["POST"])
@swag_from({
    "tags": ["Authors"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Isaac Asimov"}
                },
            },
        }
    ],
    "responses": {
        "201": {"description": "Autor criado com sucesso"},
        "400": {"description": "Payload inválido"},
        "500": {"description": "Erro interno"},
    },
})
def create_author():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Payload Vazio"}), 400

    author_schema = AuthorSchema()
    try:
        new_author = author_schema.load(data)
        db.session.add(new_author)
        db.session.commit()
        return jsonify(author_schema.dump(new_author)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Registro duplicado ou chave inválida"}), 409
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Erro interno"}), 500


@api_v1.route("/authors", methods=["GET"])
def list_authors():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = Author.query.paginate(page=page, per_page=per_page, error_out=False)
    author_schema = AuthorSchema(many=True)
    return jsonify(
        {
            "items": author_schema.dump(pagination.items),
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
        }
    ), 200


@api_v1.route("/books", methods=["POST"])
@swag_from({
    "tags": ["Books"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "example": "Foundation"},
                    "isbn": {"type": "string", "example": "9780553293357"},
                    "author_id": {"type": "integer", "example": 1},
                },
            },
        }
    ],
    "responses": {
        "201": {"description": "Livro criado com sucesso"},
        "400": {"description": "Payload inválido"},
        "500": {"description": "Erro interno"},
    },
})
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Payload Vazio"}), 400

    book_schema = BookSchema()
    try:
        new_book = book_schema.load(data)
        db.session.add(new_book)
        db.session.commit()
        return jsonify(book_schema.dump(new_book)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Registro duplicado ou chave inválida"}), 409
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Erro interno"}), 500


@api_v1.route("/books", methods=["GET"])
def list_books():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    book_schema = BookSchema(many=True)
    return jsonify(
        {
            "items": book_schema.dump(pagination.items),
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
        }
    ), 200
