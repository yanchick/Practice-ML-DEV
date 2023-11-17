from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement = True)
    username = Column(String)
    password = Column(String)












Base.metadata.create_all(engine)

user = User(username='admin2', password='god')
session.add(user)
user = User(username='admin', password='god')
session.add(user)
user = User(username='user', password='god')
session.add(user)
session.commit()

#users = session.query(User).filter(User.username=='admin').one()
#print(users.id, users.username, users.password)
#for user in users:
#     print(user.id, user.username, user.password)
