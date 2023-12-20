from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey


# Создание подключения к базе данных
engine = create_engine('sqlite:///predictions.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



class PredictionRequestDB(Base):
    __tablename__ = 'prediction_requests'

    id = Column(Integer, primary_key=True)
    case_id = Column(String)
    gender = Column(String)
    age_at_diagnosis = Column(Float)
    primary_diagnosis = Column(String)
    race = Column(String)
    idh1 = Column(Integer)
    tp53 = Column(Integer)
    atrx = Column(Integer)
    pten = Column(Integer)
    egfr = Column(Integer)
    cic = Column(Integer)
    muc16 = Column(Integer)
    pik3ca = Column(Integer)
    nf1 = Column(Integer)
    pik3r1 = Column(Integer)
    fubp1 = Column(Integer)
    rb1 = Column(Integer)
    notch1 = Column(Integer)
    bcor = Column(Integer)
    csmd3 = Column(Integer)
    smarca4 = Column(Integer)
    grin2a = Column(Integer)
    idh2 = Column(Integer)
    fat4 = Column(Integer)
    pdgfra = Column(Integer)

class PredictionResultDB(Base):
    __tablename__ = 'prediction_results'

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('prediction_requests.id'))
    prediction = Column(Integer)
    probability = Column(Float)

# Создание таблиц
Base.metadata.create_all(engine)
