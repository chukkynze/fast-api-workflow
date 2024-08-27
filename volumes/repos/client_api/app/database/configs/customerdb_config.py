from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB1_DATABASE_URL = "postgresql://clientdbuser:secret123@host.docker.internal/clientdb"

engine = create_engine(DB1_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)