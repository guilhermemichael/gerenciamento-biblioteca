from ..database import db


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    books = db.relationship(
        "Book",
        backref="author",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Author {self.name}>"
