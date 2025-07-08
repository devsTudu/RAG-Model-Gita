from sqlalchemy import create_engine, Column, Integer, String, Text, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from utils.environmentVariablesHandler import get
from utils.logger import get_logger

logger = get_logger(__name__)

# Database connection string (adjust as needed)
DATABASE_URL = get(
    "RECORDS_DATABASE_URL"
)  # Example: "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models
class TelegramUser(Base):
    __tablename__ = "telegram_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    chat_id = Column(String(50), unique=True, nullable=False)


class TelegramMessage(Base):
    __tablename__ = "telegram_messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String(50), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)


# Create tables (run once at startup)
def init_db():
    Base.metadata.create_all(bind=engine)


def ensure_tables_exist():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    required_tables = {TelegramUser.__tablename__,
                       TelegramMessage.__tablename__}
    if not required_tables.issubset(set(tables)):
        logger.info("Required tables missing. Initializing database...")
        init_db()
    else:
        logger.info("All required tables exist.")


# CRUD Functions
def add_user(username, phone, chat_id):
    session = SessionLocal()
    chat_id = str(chat_id)
    try:
        user = TelegramUser(username=username, phone=phone, chat_id=chat_id)
        session.add(user)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("Error adding user: %s", e)
        return False
    finally:
        session.close()


def add_record(chat_id, query: str, response: str):
    if not check_user_exists(chat_id):
        return False
    session = SessionLocal()
    chat_id = str(chat_id)
    try:
        message = TelegramMessage(
            chat_id=chat_id, query=query, response=response)
        session.add(message)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("Error adding message: %s", e)
        return False
    finally:
        session.close()


def check_user_exists(chat_id):
    session = SessionLocal()
    chat_id = str(chat_id)
    try:
        user = session.query(TelegramUser).filter_by(chat_id=chat_id).first()
        return user is not None
    finally:
        session.close()


def remove_user(chat_id: str):
    session = SessionLocal()

    try:
        # Check if it exists
        user = session.query(TelegramUser).filter_by(chat_id=chat_id).first()

        if user is not None:
            # Remove messages first (if you want to cascade delete, set up FK constraints)
            session.query(TelegramMessage).filter_by(chat_id=chat_id).delete()
            session.query(TelegramUser).filter_by(chat_id=chat_id).delete()

            session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("Error removing user: %s", e)
        return False
    finally:
        session.close()


ensure_tables_exist()
