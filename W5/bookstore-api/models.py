from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Junction table cho quan hệ N:M giữa Book và Author
book_author = db.Table(
    'book_author',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13))
    price_amount = db.Column(db.Integer)
    price_currency = db.Column(db.String(3))
    category_id = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(50), nullable=True)

    authors = db.relationship('Author', secondary=book_author, backref='books')

    def to_dict(self):
        return {
            "id": f"book_{self.id}", 
            "title": self.title,
            "isbn": self.isbn,
            "category_id": self.category_id,
            "genre": self.genre,
            "price": {
                "amount": self.price_amount,
                "currency": self.price_currency
            }
        }

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text)