#!/usr/bin/nev python3
""" User class module """
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """ User class """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(128), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=True)
    reset_token = Column(String(128), nullable=True)
