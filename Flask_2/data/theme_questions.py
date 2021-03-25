import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Themes(SqlAlchemyBase):
    __tablename__ = 'themes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    question = orm.relation("Questions", back_populates='theme')

    def __repr__(self):
        return self.theme