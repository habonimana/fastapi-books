from sqlalchemy.orm import registry, relationship, Session
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, select


engine = create_engine(
    'mysql+mysqlconnector://root:ndarenze@localhost:3306/books',
    echo=True
)

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Author(Base):
    __tablename__ = "authors"
    author_id = Column(Integer, primary_key=True)
    first_name= Column(String(length=50))
    last_name = Column(String(length=50))

    def __repr__(self):
        return f"<Author(author_id={self.author_id}, first_name={self.first_name}, last_name={self.last_name})>"

class Book(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True)
    title   = Column(String(length=255))
    number_of_pages = Column(Integer)

    def __repr__(self):
        return f"<Book(book_id={self.book_id}, title={self.title}, number_of_pages={self.number_of_pages})>"

class BookAuthor(Base):
    __tablename__ = "bookauthors"
    bookauthor_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.author_id'))
    book_id   = Column(Integer, ForeignKey('books.book_id'))

    author = relationship("Author")
    book   = relationship("Book")

    def __repr__(self):
        return f"<BookAuthor (bookauthor_id = '{self.bookauthor_id}', author_id={self.author_id}, book_id={self.book_id})>"

Base.metadata.create_all(engine)

# add data to the database

def add_book(book:Book, author:Author):
    with Session(engine) as session:
        # check if the book already exist
        existing_book = session.execute(select(Book).filter(Book.title== book.title, Book.number_of_pages == book.number_of_pages)).scalar()
        if existing_book:
            print("Book has already been added")
            return
        session.add(book)
        session.commit()

        # Check if the author exist
        existing_author = session.execute(select(Author).filter(Author.first_name== author.first_name, Author.last_name==author.last_name)).scalar()
        if existing_author:
            print("Author has already been added")
            pairing = BookAuthor(author_id = existing_author.author_id, book_id = book.book_id)
            session.flush()
            
        else:
            print("Author does not exist! Adding author")
            session.add(author)
            session.commit()
            pairing = BookAuthor(author_id = author.author_id, book_id = book.book_id)
            session.flush()
        session.add(pairing)
        session.commit()
        print("New pairinga add " + str(pairing))

def get_book_by_id(book_id):
    with Session(engine) as session:
        # check if the book exists
        existing_book = session.execute(select(Book).filter(Book.book_id==book_id)).scalar()
        if existing_book is None:
            raise Exception("Book does not exist")
        pairing = session.execute(select(BookAuthor).filter(BookAuthor.book_id==existing_book.book_id)).scalar()
        if pairing is None:
            raise Exception("Book does not have an author")
        author  = session.execute(select(Author).filter(Author.author_id==pairing.author_id)).scalar()
        if author is None:
            raise Exception("Author does not exist")
        if existing_book:
            return (existing_book, author)
        else:
            return False
