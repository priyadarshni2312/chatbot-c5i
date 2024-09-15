from sqlalchemy import Column, Integer, String, Text, ForeignKey, REAL
from sqlalchemy.orm import relationship
from app.db import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    
    sales = relationship("Sale", back_populates="customer")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    sales_amount = Column(REAL, nullable=False)
    sale_date = Column(String, nullable=False)

    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    customer_query = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    timestamp = Column(String, nullable=False)

