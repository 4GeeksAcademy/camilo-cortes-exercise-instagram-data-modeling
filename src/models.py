import os
import sys
import enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, ForeignKey, Column, Table, Enum
from eralchemy2 import render_er
from typing import List

Base = declarative_base()

follower = Table(
    "follower",
    Base.metadata,
    Column("user_from_id", ForeignKey("user.id")),
    Column("user_to_id", ForeignKey("user.id")),
)

class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    Comment: Mapped[List["Comment"]] = relationship()
    Post: Mapped[List["Post"]] = relationship()
    User: Mapped[List["User"]] = relationship(secondary=follower)

class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[str] = mapped_column(ForeignKey("post.id"))

class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    Comment: Mapped[List["Comment"]] = relationship()
    Media: Mapped[List["Media"]] = relationship()

class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MyEnum] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[str] = mapped_column(ForeignKey("post.id"))

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e