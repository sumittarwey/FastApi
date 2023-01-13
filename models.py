from sqlalchemy import Column, ForeignKey, Integer, String, Float,Boolean,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False, unique=True,index=True)
    price = Column(Float(precision=2), nullable=False)
    description = Column(String(200))
    store_id = Column(Integer,ForeignKey('stores.id'),nullable=False)
    def __repr__(self):
        return 'ItemModel(name=%s, price=%s,store_id=%s)' % (self.name, self.price,self.store_id)


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False, unique=True)
    items = relationship("Item",primaryjoin="Store.id == Item.store_id",cascade="all, delete-orphan")

    def __repr__(self):
        return 'Store(name=%s)' % self.name

class User(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key=True,index=True)
    full_name   = Column(String(80), nullable=False)
    username    = Column(String(100),nullable=False,unique=True)
    password    = Column(String(80), nullable=False)
    is_active   = Column(Boolean, unique=False,default=True)
    created     = Column(DateTime, server_default=func.now())

 

   





