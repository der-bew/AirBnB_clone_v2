#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all", backref="state")
    else:
        name = ""

        @property
        def cities(self):
            """
            getter attribute cities that returns the list of
            City instances with state_id equals to the current State.id
            """
            rets = []
            for x in models.storage.all(State).values():
                if x.state_id == self.id:
                    rets.append(x)
            return rets
