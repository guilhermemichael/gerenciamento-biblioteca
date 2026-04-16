from ..database import ma
from ..models.author import Author
from ..models.book import Book


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
        include_fk = True


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True
        include_fk = True

    books = ma.Nested(BookSchema, many=True, exclude=("author_id",))
