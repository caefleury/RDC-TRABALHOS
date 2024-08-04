from sqlalchemy import create_engine, MetaData
from database import db

db.drop_all()
db.create_all()