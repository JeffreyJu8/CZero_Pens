from database import Base, engine
from models import Inventory

print("Creating database...")

Base.metadata.create_all(engine)