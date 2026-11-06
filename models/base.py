from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config.settings import settings


engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=False
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_database():
    import models.forex
    import models.crypto
    import models.economic
    import models.pipeline

    Base.metadata.create_all(bind=engine)
