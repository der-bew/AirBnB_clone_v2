#!/usr/bin/python3
"""SQL db engine"""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """SQL database class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializing db engine"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(user, passwd, host, db),
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.env)

    def all(self, cls=None):
        """All or single object"""
        cls_dict = {}
        if cls:
            query = self.__session.query(cls)
            for q in query:
                key = "{}.{}".format(type(q).__name__, q.id)
                cls_dict[key] = q
        else:
            cls_list = [Amenity, City, Place, Review, State, User]
            for x in cls_list:
                query = self.__session.query(x)
                for q in query:
                    key = "{}.{}".format(type(q).__name__, q.id)
                    cls_dict[key] = q
        return cls_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload db"""
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()
