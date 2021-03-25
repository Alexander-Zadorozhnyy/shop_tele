from Flask_2.data import db_session
from Flask_2.data.shop_items import Items
from Flask_2.data.users import User


def create_basket(title, content, user_id):
    basket = Basket(title=title, content=content,
                    user_id=user_id)
    db_sess = db_session.create_session()
    db_sess.add(basket)
    db_sess.commit()


def create_item(name, content, about):
    item = Items(name=name, content=content,
                 about=about)
    db_sess = db_session.create_session()
    db_sess.add(item)
    db_sess.commit()


def edit_item(id_item, content=None, name=None, about=None):
    db_sess = db_session.create_session()
    item = db_sess.query(Items).filter(Items.id == id_item).first()
    if content:
        item.content = content
    if name:
        item.name = name
    if about:
        item.about = about
    db_sess.commit()


def delete_item(item_id):
    db_sess = db_session.create_session()
    item = db_sess.query(Items).filter(Items.id == item_id).first()
    db_sess.delete(item)
    db_sess.commit()
