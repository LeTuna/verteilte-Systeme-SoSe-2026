from db import Base, engine
from models.db_models import PollDB, OptionDB, VoteDB

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Database initialized successfully")