from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def build_db_url() -> str:
    return "postgresql+psycopg2://tm_user:tm_pass@postgres:5432/threat_modeling"


engine = create_engine(build_db_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
