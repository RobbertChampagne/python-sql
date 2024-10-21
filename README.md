# Python-SQL

**SQLAlchemy**:<br>
Is a comprehensive SQL toolkit and Object-Relational Mapping (ORM) library for Python.<br>

**Pydantic**:<br>
Is a data validation and settings management library using Python type annotations.<br>

**SQLModel** (SQLAlchemy + Pydantic):<br>
Is a library that combines the best features of SQLAlchemy and Pydantic.<br> 
It simplifies the creation of SQLAlchemy models using Pydantic for data validation.<br>


**ORM** (Object-Relational Mapping)<br>
Allows you to interact with the database using Python objects instead of writing raw SQL queries.<br>
This makes the code more readable and maintainable.<br>

```Python
def get_book_by_id_orm(book_id: int):
    with Session(engine) as session:
        item = session.exec(select(Book).where(Book.id == book_id)).first()
        return item
```

**Raw SQL**<br>
Queries are written directly in SQL and executed against the database.<br> 
This provides more control over the queries but can be less readable and harder to maintain.<br>

```Python
def get_book_by_id_raw_sql(book_id: int):
    with Session(engine) as session:
        result = session.execute(text(f"SELECT * FROM book WHERE id = {book_id}"))
        item = result.fetchone()
        return item
```

----

### Virtual Environments:

**Run the following command to create a virtual environment:**
```Bash
python -m venv python-sql
```

**Activate the Virtual Environment:**
```Bash
python-sql\Scripts\activate
```

**Install Packages:**
```Bash
pip install sqlmodel
```

**Deactivate the Virtual Environment:**
```Bash
deactivate
```

**Export the installed packages to a requirements.txt file:**
```Bash
pip freeze > requirements.txt
```

**Install packages from requirements.txt:**
```Bash
pip install -r requirements.txt
```

**To list all virtual environments created using venv or other tools like virtualenv, you can use:**
```Bash
dir /s /b activate
```

---
### Project structure:

```
python-sql/
├── src/
│   ├── main.py
│   └── models.py
│     
├── tests/
│   ├── conftest.py
│   ├── test_script1.py
│   └── test_loggingSetup.py
├── .gitignore
├── pytest.ini
└── README.md
```

### src/:
`main.py`
```Python
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

```
**Output:**
```Bash
> python src/main.py
Raw SQL: (1, 'Book One', 'Summary of Book One', 1)
ORM SQL: author_id=1 id=1 summary='Summary of Book One' title='Book One'
```

---
