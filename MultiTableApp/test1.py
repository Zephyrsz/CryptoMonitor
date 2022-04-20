from datetime import datetime
# from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import (
    Column,
)
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    String
)

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(BigInteger, primary_key=True)
    created_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_time = Column(DateTime, nullable=False, default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    name = Column(String, nullable=False)

class CustomerSchema1(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Customer

class CustomerSchema2(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Customer
        exclude = ('created_time',)

cs1 = CustomerSchema1()
print('CustomerSchema1 instantiated')
cs2 = CustomerSchema2()
print('CustomerSchema2 instantiated')