import os
import datetime
import atexit
# from uuid import UUID

from sqlalchemy import Integer, String, DateTime, func, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedColumn, mapped_column, relationship, Mapped


POSTGRES_USER = os.getenv('POSTGRES_USER', 'ad_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'ad_password')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'ad_site')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):

    __tablename__ = 'ad_users'
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: MappedColumn[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    password: MappedColumn[str] = mapped_column(String(60), nullable=False)
    email: MappedColumn[str] = mapped_column(String(50), nullable=False, index=True)
    creation_time: MappedColumn[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    ad: Mapped[list["Ad"]] = relationship("Ad", back_populates="author", cascade="all, delete")

    @property
    def id_json(self):
        return {'id': self.id}

    @property
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'creation_time': self.creation_time.isoformat()
        }

class Ad(Base):
    __tablename__ = 'ads'

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    header: MappedColumn[str] = mapped_column(String(100), nullable=False, index=True)
    description: MappedColumn[str] = mapped_column(String(500))
    creation_time: MappedColumn[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("ad_users.id"), nullable=False)
    author: Mapped[User] = relationship("User", back_populates="ad")

    @property
    def id_json(self):
        return {'id': self.id}

    @property
    def json(self):
        return {
            'id': self.id,
            'header': self.header,
            'description': self.description,
            'creation_time': self.creation_time.isoformat(),
            'user_id': self.user_id
        }
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
atexit.register(engine.dispose)
