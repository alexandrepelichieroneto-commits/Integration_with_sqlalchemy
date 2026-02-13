import sqlalchemy as sqlA
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import inspect
from sqlalchemy import create_engine
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
        return f"Address (id={self.id}, email_address={self.email_address})"

print(User.__tablename__)
print(Address.__tablename__)


#conexão com o banco de dados
engine = create_engine("sqlite://")

#criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

#depreciado - será removido em futuro release
#print(engine.table_names())

#investiga o esquema de banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)


with Session(engine) as session:
    alexandre = User(
        name='alexandre',
        fullname='Alexandre Pelichiero',
        address=[Address(email_address='alexandrepelichiero@outlook.com')]
    )

    sandy = User(
        name='sandy',
        fullname='Sandy Cardaso',
        address=[Address(email_address='sandy65464646545@gmail.com.br'),
                 Address(email_address='sandy6546464654587878922@gmail.com.org')]
    )

    patrick = User(
        name='patrick',
        fullname='Patrick Cardoso'
    )

    #enviando para o Banco de Dados (persistência de dados)
    session.add_all([alexandre, sandy, patrick])

    session.commit()

print("\nRecuperando usuários a partir de condição de filtragem:")
stmt = select(User).where(User.name.in_(['alexandre', 'patrick']))
for user in session.scalars(stmt):
    print(user)


print("\nRecuperando endereços de email de Sandy:")
stmt_address = select(Address).where(Address.user_id.in_([2]))
for address in session.scalars(stmt_address):
    print(address)


print("\nRecuperando informações de maneira ordenada:")
stmt_order = select(User).order_by(User.fullname.desc())
for result in session.scalars(stmt_order):
    print(result)


stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):
    print(result)


#print(select(User.fullname, Address.email_address).join_from(Address, User))


print("\nExecutando statement a partir da connection")
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
for result in results:
    print(result)


print("\nTotal de instâncias em User")
stmt_count = select(func.count('*')).select_from(User)
for result in session.scalars(stmt_count):
    print(result)


