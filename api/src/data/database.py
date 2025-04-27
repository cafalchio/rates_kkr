from sqlalchemy import create_engine

DATABASE = "sqlite:////home/cafa/rates_kkr/etl/src/database.db"

engine_db = create_engine(DATABASE)