from operator import and_

from saleapp.models import Category, Book, User, Receipt, ReceiptDetails, Author
from saleapp import db
from flask_login import current_user
from sqlalchemy import func, extract
import hashlib


def load_categories():
    return Category.query.all()


def load_books(category_id=None, kw=None):
    query = Book.query.filter(Book.active.__eq__(True))

    if category_id:
        query = query.filter(Book.category_id.__eq__(category_id))

    if kw:
        query = query.filter(Book.name.contains(kw))

    return query.all()


def get_book_by_id(book_id):
    return Book.query.get(book_id)

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_receipt(cart):
    if cart:
        r = Receipt(user_id=1)
        db.session.add(r)
        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, book_id=c['id'])
            db.session.add(d)

        db.session.commit()


def count_book_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Book.id)) \
        .join(Book, Book.category_id.__eq__(Category.id), isouter=True) \
        .group_by(Category.id).order_by(-Category.name).all()

def stats_revenue_by_prod(from_date=None, to_date=None, kw=None):
    data = db.session.query(Category.name,func.month(Receipt.created_date),
                            func.sum(ReceiptDetails.quantity*ReceiptDetails.price)) \
        .join(Receipt,Receipt.id == ReceiptDetails.receipt_id) \
        .join(Book, Book.id == ReceiptDetails.book_id) \
        .join(Category, Book.category_id == Category.id) \
        .group_by(func.month(Receipt.created_date)) \
        .order_by(func.month(Receipt.created_date))
    if kw:
        data = data.filter(Category.name.__eq__(kw))
    if from_date and to_date:
        data = data.filter(and_(extract('month', Receipt.created_date) >= extract('month', from_date),
                                extract('month', Receipt.created_date) <= extract('month', to_date)))


    return data.all()

# def stats_revenue_by_prod(kw=None, from_date=None, to_date=None):
#     query = db.session.query(func.month(Receipt.created_date),
#                             func.sum(ReceiptDetails.quantity * ReceiptDetails.price)) \
#         .join(Receipt) \
#         .filter(Receipt.id == ReceiptDetails.receipt_id) \
#         .join(Book) \
#         .filter(Book.id == ReceiptDetails.book_id) \
#         .join(Category) \
#         .filter(Category.id == Book.id) \
#         .group_by(func.month(Receipt.created_date)) \
#         .order_by(func.month(Receipt.created_date))
#     if kw:
#         query = query.filter(Category.name.contains(kw))
#
#     if from_date:
#         query = query.filter(Receipt.created_date.__ge__(from_date))
#
#     if to_date:
#         query = query.filter(Receipt.created_date.__le__(to_date))
#
#     return query.group_by(Book.id).all()

def Stat_on_fre_book_by_month(year=None):
    query = db.session.query(Book.id, Book.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.price)) \
        .join(ReceiptDetails, ReceiptDetails.book_id.__eq__(Book.id)) \
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))
    query = query.filter(Book.name.contains())

    return query.group_by(Book.id).all()

def statistic_book_using_frequency_month(from_month=None, to_month=None, keyword=None):
    data = db.session.query(func.month(Receipt.created_date),
                            func.sum(ReceiptDetails.quantity)) \
        .join(Receipt) \
        .filter(Receipt.id == ReceiptDetails.receipt_id) \
        .join(Book) \
        .filter(Book.id == ReceiptDetails.book_id) \
        .group_by(func.month(Receipt.created_date)) \
        .order_by(func.month(Receipt.created_date))

    if keyword:
        data = data.filter(Book.name.__eq__(keyword))

    if from_month and to_month:
        data = data.filter(and_(extract('month', Receipt.created_date) >= extract('month',from_month),
                                extract('month', Receipt.created_date) <= extract('month',to_month)))
    return data.all()

if __name__ == '__main__':
    from saleapp import app

    with app.app_context():
        print(stats_revenue_by_prod())
