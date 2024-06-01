#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.operators import endswith_op

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Create a User object and save it to the database
        Args:
            email (str): user's email address
            hashed_password (str): password hashed by bcrypt's hashpw
        Return:
            Newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Return a user who has an attribute matching the attributes passed
        as arguments
        Args:
            attributes (dict): a dictionary of attributes to match the user
        Return:
            matching user or raise error
        """
        all_users = self._session.query(User)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError
            for user in all_users:
                if getattr(user, key) == value:
                    return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user in the database
        Args:
            user_id (int): user id
            attributes (dict): a dictionary of attributes to update
        Return:
            None
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError()
            setattr(user, key, value)
        self._session.commit()
