from flask import Blueprint, request, jsonify
from flasgger import swag_from

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

    try:
        author_schema = AuthorSchema()
        new_author = author_schema.load(data)
        db.session.add(new_author)
        db.session.commit()
        return jsonify(author_schema.dump(new_author)), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({"error": str(exc)}), 500


@api_v1.route("/authors", methods=["GET"])
def list_authors():
    authors = Author.query.all()
    author_schema = AuthorSchema(many=True)
    return jsonify(author_schema.dump(authors)), 200


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

    try:
        book_schema = BookSchema()
        new_book = book_schema.load(data)
        db.session.add(new_book)
        db.session.commit()
        return jsonify(book_schema.dump(new_book)), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({"error": str(exc)}), 500


@api_v1.route("/books", methods=["GET"])
def list_books():
    books = Book.query.all()
    book_schema = BookSchema(many=True)
    return jsonify(book_schema.dump(books)), 200
