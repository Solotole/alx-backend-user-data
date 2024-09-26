#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User, Base



VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id',
                'reset_token']


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adding a new user into the database
        """
        if not email or not hashed_password:
            return
        new_user: User = User(email=email, hashed_password=hashed_password)
        session: Session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """querying and returning id or error otherwise"""
        if not kwargs or any(x not in VALID_FIELDS for x in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """updating user credentials based on user_id
        """
        try:
            find_user: User = self.find_user_by(id=user_id)
            # for key in kwargs.keys():
            # if key not in VALID_FIELDS:
            # raise ValueError
            for key, value in kwargs.items():
                if not hasattr(find_user, key):
                    raise ValueError(f"User has no attribute '{key}'")
                setattr(find_user, key, value)
            self._session.commit()
        except NoResultFound:
            raise ValueError(f"User with id {user_id} not found")
        except InvalidRequestError:
            raise ValueError("Invalid request")
        except Exception:
            raise ValueError('')
