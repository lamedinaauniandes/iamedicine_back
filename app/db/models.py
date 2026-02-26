from app.db.database import BASE
from sqlalchemy import Column, Integer,String, Boolean,DateTime
from datetime import datetime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship 

class User(BASE):
    __tablename__= "user"

    id = Column(Integer,primary_key=True,autoincrement=True)
    nombre = Column(String)
    username= Column(String)
    password = Column(String)
    apellido = Column(String)
    direccion = Column(String)
    telefono = Column(Integer)
    correo = Column(String,unique=True)
    tipo = Column(Integer)
    creacion = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    estado = Column(Boolean,default=False)
    venta = relationship("Venta",backref="user",cascade="delete,merge")

class Venta(BASE):
    __tablename__ = "venta"
    id = Column(Integer,primary_key=True,autoincrement=True)
    usuario_id = Column(Integer,ForeignKey("user.id",ondelete="CASCADE"))
    venta = Column(Integer)
    ventas_productos = Column(Integer)