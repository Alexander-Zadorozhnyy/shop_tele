import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Basket(SqlAlchemyBase):
    __tablename__ = 'basket'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    item_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("items.id"))
    item = orm.relation('Items')