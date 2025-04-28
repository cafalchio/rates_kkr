from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DATABASE = "sqlite:////home/cafa/rates_kkr/etl/src/database.db"

engine_db = create_engine(DATABASE)
session = Session(engine_db)
