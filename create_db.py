from sqlmodel import SQLModel
from models import Infovaluation
from database import engine

print("CREATING DATABASE.....")

SQLModel.metadata.create_all(engine)