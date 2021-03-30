import sqlalchemy
from .db_session import SqlAlchemyBase


category_to_items = sqlalchemy.Table(
    'category_to_items',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('item', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('items.id')),
    sqlalchemy.Column('category', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('category.id'))
)


class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

