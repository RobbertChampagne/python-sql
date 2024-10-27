# python src/main.py

from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.sql import text, func, case
from models import Author, Book

# SQLite setup
DATABASE_URL = "sqlite:///./sqliteDB.db"
engine = create_engine(DATABASE_URL)

def raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT * FROM book"))
        return result.fetchall()

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

# Group By: Grouping books by author.
# [('Author One', 2), ('Author Two', 2)]
def get_books_group_by_author_orm():
    with Session(engine) as session:
        result = session.exec(select(Author.name, func.count(Book.id)).join(Book).group_by(Author.name)).all()
        return result

def get_books_group_by_author_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT author.name, COUNT(book.id) FROM author JOIN book ON author.id = book.author_id GROUP BY author.name"))
        return result.fetchall()

# Order By: Ordering books by title.
''' 
    [ 
        Book(id=4, summary='Summary of Book Four', title='Book Four', author_id=2), 
        Book(id=1, summary='Summary of Book One', title='Book One', author_id=1), 
        Book(id=3, summary='Summary of Book Three', title='Book Three', author_id=2), 
        Book(id=2, summary='Summary of Book Two', title='Book Two', author_id=1)
    ]
'''

def get_books_order_by_title_orm():
    with Session(engine) as session:
        result = session.exec(select(Book).order_by(Book.title)).all()
        return result

def get_books_order_by_title_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT * FROM book ORDER BY title"))
        return result.fetchall()

# Having: Filtering authors with multiple books.
# [('Author One', 2), ('Author Two', 2)]
def get_authors_having_multiple_books_orm():
    with Session(engine) as session:
        result = session.exec(select(Author.name, func.count(Book.id)).join(Book).group_by(Author.name).having(func.count(Book.id) > 1)).all()
        return result

def get_authors_having_multiple_books_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT author.name, COUNT(book.id) FROM author JOIN book ON author.id = book.author_id GROUP BY author.name HAVING COUNT(book.id) > 1"))
        return result.fetchall()

# Limit: Limiting the number of books returned.
# get_books_limit_raw_sql(2)
# [(1, 'Book One', 'Summary of Book One', 1), (2, 'Book Two', 'Summary of Book Two', 1)]
def get_books_limit_orm(limit: int):
    with Session(engine) as session:
        result = session.exec(select(Book).limit(limit)).all()
        return result

def get_books_limit_raw_sql(limit: int):
    with Session(engine) as session:
        result = session.execute(text(f"SELECT * FROM book LIMIT {limit}"))
        return result.fetchall()

# Aliasing: Using aliases for tables.
# [('Book One', 'Author One'), ('Book Two', 'Author One'), ('Book Three', 'Author Two'), ('Book Four', 'Author Two')]
def get_books_with_author_alias_orm():
    with Session(engine) as session:
        author_alias = Author.__table__.alias("a")
        result = session.exec(select(Book.title, author_alias.c.name).join(author_alias, Book.author_id == author_alias.c.id)).all()
        return result

def get_books_with_author_alias_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT book.title, a.name FROM book JOIN author AS a ON book.author_id = a.id"))
        return result.fetchall()

# Joins: Joining books with authors.
# [('Book One', 'Author One'), ('Book Two', 'Author One'), ('Book Three', 'Author Two'), ('Book Four', 'Author Two')]
def get_books_with_authors_orm():
    with Session(engine) as session:
        result = session.exec(select(Book.title, Author.name).join(Author)).all()
        return result

def get_books_with_authors_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT book.title, author.name FROM book JOIN author ON book.author_id = author.id"))
        return result.fetchall()

# Unions: Combining results from books and authors.
# [('Author One',), ('Author Two',), ('Book Four',), ('Book One',), ('Book Three',), ('Book Two',)]
def get_books_and_authors_union_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT title FROM book UNION SELECT name FROM author"))
        return result.fetchall()

# String Functions: Using string functions like UPPER.
# [('BOOK ONE',), ('BOOK TWO',), ('BOOK THREE',), ('BOOK FOUR',)]
def get_books_title_uppercase_orm():
    with Session(engine) as session:
        result = session.exec(select(func.upper(Book.title))).all()
        return result

def get_books_title_uppercase_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT UPPER(title) FROM book"))
        return result.fetchall()

# Case Statements: Using CASE statements.
# [('Book One', '1 or less'), ('Book Two', 'More than 1'), ('Book Three', 'More than 1'), ('Book Four', 'More than 1')]
def get_books_with_case_statement_orm():
    with Session(engine) as session:
        case_statement = case(
            (Book.id > 1, "More than 1"), (Book.id <= 1, "1 or less"),
            else_="Unknown").label("description")
        result = session.exec(select(Book.title, case_statement)).all()
        return result

def get_books_with_case_statement_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT title, CASE WHEN id > 1 THEN 'More than 1' WHEN id <= 1 THEN '1 or less' ELSE 'Unknown' END FROM book"))
        return result.fetchall()

# Subqueries: Using subqueries.
# [('Author One', 2), ('Author Two', 2)]
def get_books_with_subquery_orm():
    with Session(engine) as session:
        subquery = select(func.count(Book.id)).where(Book.author_id == Author.id).scalar_subquery() # to create a subquery that returns a single scalar value
        result = session.exec(select(Author.name, subquery.label("book_count"))).all()
        return result

def get_books_with_subquery_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT author.name, (SELECT COUNT(*) FROM book WHERE book.author_id = author.id) AS book_count FROM author"))
        return result.fetchall()

# Window Functions: Using window functions like ROW_NUMBER.
# [('Book Four', 1), ('Book One', 2), ('Book Three', 3), ('Book Two', 4)]
def get_books_with_row_number_orm():
    with Session(engine) as session:
        # Create the query
        query = select(Book.title, func.row_number().over(order_by=Book.title).label("row_number"))
        
        # Execute the query and fetch all results
        result = session.exec(query).all()
        
        return result

def get_books_with_row_number_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("SELECT title, ROW_NUMBER() OVER (ORDER BY title) FROM book"))
        return result.fetchall()

# Common Table Expressions (CTEs): Using CTEs.
# ['Book One', 'Book Two', 'Book Three', 'Book Four']
def get_books_with_cte_orm():
    with Session(engine) as session:
        cte = select(Book).cte("book_cte")
        result = session.exec(select(cte.c.title).select_from(cte)).all()
        return result

def get_books_with_cte_raw_sql():
    with Session(engine) as session:
        result = session.execute(text("WITH book_cte AS (SELECT * FROM book) SELECT title FROM book_cte"))
        return result.fetchall()

# Temporary Tables: Creating and querying temporary tables.
# [(1, 'Book One', 'Summary of Book One', 1), (2, 'Book Two', 'Summary of Book Two', 1), (3, 'Book Three', 'Summary of Book Three', 2), (4, 'Book Four', 'Summary of Book Four', 2)]
def create_temp_table_raw_sql():
    with Session(engine) as session:
        session.execute(text("CREATE TEMPORARY TABLE temp_books AS SELECT * FROM book"))
        result = session.execute(text("SELECT * FROM temp_books"))
        return result.fetchall()

def create_book(title: str, summary: str, author_id: int):
    with Session(engine) as session:
        book = Book(title=title, summary=summary, author_id=author_id)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

def update_book(book_id: int, title: str = None, summary: str = None):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book:
            if title:
                book.title = title
            if summary:
                book.summary = summary
            session.add(book)
            session.commit()
            session.refresh(book)
            return book
        else:
            return None

if __name__ == "__main__":
    # Create a new book
    #new_book = create_book("Book Title 2", "Book Summary", 1)
    #print(f"Created Book: {new_book}")
    
    # Update the book
    #updated_book = update_book(5, title="Updated Book Title")
    #print(f"Updated Book: {updated_book}")
    
    result = raw_sql()
    print(result)
