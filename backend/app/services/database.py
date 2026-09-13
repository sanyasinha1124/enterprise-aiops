from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db():
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """))
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                amount REAL NOT NULL,
                days_since_purchase INTEGER NOT NULL,
                status TEXT NOT NULL
            )
        """))
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS support_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                issue TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """))

        count = connection.execute(text("SELECT COUNT(*) FROM customers")).scalar_one()
        if count == 0:
            connection.execute(
                text("INSERT INTO customers(id,name,email) VALUES "
                     "(1001,'Aarav Mehta','aarav@example.com'),"
                     "(1002,'Priya Shah','priya@example.com')")
            )
            connection.execute(
                text("INSERT INTO orders(id,customer_id,product,amount,days_since_purchase,status) VALUES "
                     "(5001,1001,'Wireless Headphones',4999,12,'delivered'),"
                     "(5002,1002,'Smart Watch',7999,45,'delivered')")
            )


def query_one(sql: str, params: dict):
    with engine.begin() as connection:
        row = connection.execute(text(sql), params).mappings().first()
        return dict(row) if row else None


def insert_ticket(customer_id: int, issue: str):
    with engine.begin() as connection:
        result = connection.execute(
            text(
                "INSERT INTO support_tickets(customer_id,issue,status) "
                "VALUES (:customer_id,:issue,'open')"
            ),
            {"customer_id": customer_id, "issue": issue},
        )
        return result.lastrowid
