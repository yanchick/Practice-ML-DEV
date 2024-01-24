from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    __tableargs__ = {
        'comment': 'Таблица с информацией о пользователях'
    }

    email = Column(
        String,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String, comment='Логин пользователя')
    password = Column(String, comment='Пароль пользователя')

    def __repr__(self):
        return f'{self.email} {self.name} {self.password}'


engine = create_engine("jdbc:postgresql://localhost:5432/postgres")
Base.metadata.create_all(engine)
