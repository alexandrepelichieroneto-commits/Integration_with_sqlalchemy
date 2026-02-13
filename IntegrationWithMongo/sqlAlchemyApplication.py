import sqlalchemy as sqlA
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"
    #atributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"

class Address(Base):
    __tablename__ = "address"
    #atributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship(
        "User", back_populates="address"
    )

    def __repr__(self):
        return f"Address (id={self.id}, email={self.email_address})"

print(User.__tablename__)
print(Address.__tablename__)
