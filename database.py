from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine=create_engine("postgresql://postgres:FCBarcelona1899@localhost/CZero_Pens",
                     echo=True)

connection = engine.connect()
Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)

