import databases
from sqlalchemy import create_engine, MetaData

DB2_DATABASE_URL = "mysql://clientdbuser:secret123@host.docker.internal/clientdb"

db2_database = databases.Database(DB2_DATABASE_URL)
db2_metadata = MetaData()

db2_engine = create_engine(DB2_DATABASE_URL)
db2_metadata.create_all(db2_engine)