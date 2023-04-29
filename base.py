from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Select
from sqlalchemy import Table, Column, Integer, String

from sqlalchemy import ForeignKey

from pprint import pprint


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    address: Mapped[List["Address"]] = relationship(back_populates="user")

    def greeting(self) -> str:
        return f'Hello, {self.name}'

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["User"] = relationship(back_populates="address")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r}"


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        ivan = User(name='Dron', fullname='Andrey Bodosov')
        pprint(ivan)
        session.add(ivan)
        ivan.address.append(Address(email_address='a.bodosov@gmail.com'))
        ivan.address.append(Address(email_address='hulu@yandex.ru'))
        stmt = Select(User).where(User.name == 'Dron')
        user = session.scalar(stmt)
        pprint(user.address)
        session.commit()
