import uuid
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]]
    password: Mapped[Optional[str]]

    def set_user(self, values):
        self.username = values.username
        self.email = values.email
        self.password = values.password

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, password={self.password!r})"

class UserTableSchema(BaseModel):
    username: str
    email: str
    password: str



