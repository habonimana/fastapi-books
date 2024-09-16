from fastapi import FastAPI, HTTPException
from . import schemas
from . import database

app = FastAPI()

@app.get("/")
def get_root():
    return "Welcome to the books api"

@app.get("/book/{book_id}")
async def get_book_by_id(book_id: int):
    try:
        bookauthor = database.get_book_by_id(book_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=repr(e))
    return bookauthor


@app.post("/book/")
def create_book(request: schemas.BookAutoPayload):
    database.add_book(convert_into_book_db_model(request.book), convert_into_author_db_model(request.author))
    return f"New book added | Title:  {request.book.title} {str(request.book.number_of_pages)} \n New Author added  Author: {request.author.first_name} {request.author.last_name}"


def convert_into_book_db_model(book:schemas.Book):
    return database.Book(title = book.title, number_of_pages = book.number_of_pages)

def convert_into_author_db_model(author: schemas.Author):
    return database.Author(first_name = author.first_name, last_name = author.last_name)

