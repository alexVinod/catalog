import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class OurUsers(Base):
    __tablename__ = 'ourUsers'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True)
    picture = Column(String(3000), nullable=False)


class BookStoreCategory(Base):
    __tablename__ = 'book_store_category'

    id = Column(Integer, primary_key=True)
    category = Column(String(500), nullable=False, unique=True)

    ourUser_id = Column(Integer, ForeignKey('ourUsers.id'))
    ourUsers = relationship(OurUsers)

    @property
    def serialize(self):
        return {
            'category': self.category,
            'id': self.id
        }


class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(300), nullable=False)
    bookType = Column(String(200), nullable=False)
    description = Column(String(3000), nullable=False)
    # publishedDate = Column(String(100),
    # nullable=False, default=datetime.utcnow)
    publishedDate = Column(String(100), nullable=False)
    publisher = Column(String(200), nullable=False)
    imageLinks = Column(String(3000), nullable=False)
    infoLink = Column(String(3000), nullable=False)
    category_id = Column(Integer, ForeignKey('book_store_category.id'))
    category = relationship(BookStoreCategory)
    # bookSamples = Column(String(3000), nullable=True)

    ourUser_id = Column(Integer, ForeignKey('ourUsers.id'))
    ourUsers = relationship(OurUsers)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'bookType': self.bookType,
            'description': self.description,
            'publishedDate': self.publishedDate,
            'publisher': self.publisher,
            'imageLinks': self.imageLinks,
            'infoLink': self.infoLink
        }

engine = create_engine('sqlite:///books.db')

Base.metadata.create_all(engine)

# id = Column(Integer, primary_key=True)
# title = Column(String(250), nullable=False)
# author = Column(String(300), nullable=False)
# categories = Column(String(200), nullable=False)
# bookType = Column(String(200), nullable=False)
# contentVersion = Column(String(200), nullable=False)
# description = Column(String(3000), nullable=False)
# publishedDate = Column(db.DateTime, nullable=False, default=datetime.utcnow)
# publisher   = Column(String(200), nullable=False)
# lengthOfPages = Column(String(200), nullable=False)
# imageLinks = Column(String(3000), nullable=False)
# infoLink = Column(String(3000), nullable=False)
# averageRating = Column(String(30), nullable=False)
