# python src/main.py
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.sql import text
from models import Author, Book

# SQLite setup
DATABASE_URL = "sqlite:///./orm.db"
engine = create_engine(DATABASE_URL)

# Function to execute raw SQL query
def get_book_by_id_raw_sql(book_id: int):
    with Session(engine) as session:
        result = session.execute(text(f"SELECT * FROM book WHERE id = {book_id}"))
        item = result.fetchone()
        return item

# Function to execute ORM query
def get_book_by_id_orm(book_id: int):
    with Session(engine) as session:
        item = session.exec(select(Book).where(Book.id == book_id)).first()
        return item

if __name__ == "__main__":
    book_raw_sql = get_book_by_id_raw_sql(1)
    book_orm_sql = get_book_by_id_orm(1)
    print("Raw SQL:", book_raw_sql)
    print("ORM SQL:", book_orm_sql)
