# python src/models.py
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session

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
    
    author: Author = Relationship(back_populates="books") 
    
# SQLite setup
DATABASE_URL = "sqlite:///./orm.db"
engine = create_engine(DATABASE_URL)

# Create the database tables
SQLModel.metadata.create_all(engine)

# Predefined data points
authors = [
    Author(name="Author One", bio="Bio of Author One"),
    Author(name="Author Two", bio="Bio of Author Two"),
]

books = [
    Book(title="Book One", summary="Summary of Book One", author_id=1),
    Book(title="Book Two", summary="Summary of Book Two", author_id=1),
    Book(title="Book Three", summary="Summary of Book Three", author_id=2),
]

# Insert data into the database
with Session(engine) as session:
    for author in authors:
        session.add(author)
    session.commit()  # Commit authors first to get their IDs

    for book in books:
        session.add(book)
    session.commit()