from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = os.getenv("database")

engine_db = create_engine(DATABASE)
session = Session(engine_db)
