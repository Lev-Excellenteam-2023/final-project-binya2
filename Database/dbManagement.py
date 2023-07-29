import datetime
import uuid
from typing import List

from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, Mapped, mapped_column
from enum import Enum as myEnum

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    uploads: Mapped[List["Upload"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"

class Status(myEnum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    DONE = 'done'
    FAILED = 'failed'

class Upload(Base):
    __tablename__ = 'uploads'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(nullable=False)
    filename: Mapped[str] = mapped_column(nullable=False)
    upload_time: Mapped[datetime] = mapped_column(nullable=False)
    finish_time: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[Status] = mapped_column(nullable=False, default = Status.PENDING)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)

    user: Mapped["User"] = relationship(back_populates="uploads", cascade='all')

    def __init__(self, filename: str, uid: str, upload_time: datetime):
        self.uid = uid
        self.filename = filename
        self.upload_time = upload_time


    def __repr__(self):
        return f"<Upload(id={self.id}, uid='{self.uid}', filename='{self.filename}', " \
               f"upload_time='{self.upload_time}', finish_time='{self.finish_time}', " \
               f"status='{self.status}', user_id={self.user_id})>"

    def upload_path(self) -> str:
        return f"/uploads/{self.uid}/{self.filename}"



    def set_failed(self, error_message: str) -> None:
        """todo"""
