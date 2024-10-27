# python src/models.py
import os
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select
from datetime import datetime

class Author(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    bio: str = Field(max_length=100)
    
    books: list["Book"] = Relationship(back_populates="author") 

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    summary: str = Field(max_length=100)
    author_id: int = Field(foreign_key="author.id")
    updated_at: datetime = Field(default=None, nullable=True)
    
    author: Author = Relationship(back_populates="books") 
    
# SQLite setup
DATABASE_URL = "sqlite:///./sqliteDB.db"
engine = create_engine(DATABASE_URL)

# Check if the database file exists
if not os.path.exists("./sqliteDB.db"):
    # Create the database tables
    SQLModel.metadata.create_all(engine)
    print("Database created")

    # Insert predefined data points
    authors = [
        Author(name="Author One", bio="Bio of Author One"),
        Author(name="Author Two", bio="Bio of Author Two"),
    ]

    books = [
        Book(title="Book One", summary="Summary of Book One", author_id=1),
        Book(title="Book Two", summary="Summary of Book Two", author_id=1),
        Book(title="Book Three", summary="Summary of Book Three", author_id=2),
        Book(title="Book Four", summary="Summary of Book Four", author_id=2),
    ]

# Insert data into the database if it doesn't already exist
with Session(engine) as session:
    # Check if authors already exist
    existing_authors = session.exec(select(Author)).all()
    if not existing_authors:
        for author in authors:
            session.add(author)
        session.commit()  # Commit authors first to get their IDs

    # Check if books already exist
    existing_books = session.exec(select(Book)).all()
    if not existing_books:
        for book in books:
            session.add(book)
        session.commit()