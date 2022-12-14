from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from saleapp import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    ADMIN = 1
    BOOK_SELLER = 2
    WAREHOUSE_MANGER = 3
    USER = 4


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


book_tag = db.Table('book_tag',
                    Column('book_id', ForeignKey('book.id'), nullable=False, primary_key=True),
                    Column('tag_id', ForeignKey('tag.id'), nullable=False, primary_key=True))


book_author = db.Table('book_author',
                    Column('book_id', ForeignKey('book.id'), nullable=False, primary_key=True),
                    Column('author_id', ForeignKey('author.id'), nullable=False, primary_key=True))

class Book(BaseModel):
    __tablename__ = 'book'

    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(500))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship('Tag', secondary='book_tag', lazy='subquery',
                        backref=backref('book', lazy=True))
    receipt_details = relationship('ReceiptDetails', backref='book', lazy=True)
    goodreceived_details = relationship('GoodReceived_Detail', backref='book', lazy=True)
    author = relationship('Author', 'book_author', backref='book', lazy=True)

    def __str__(self):
        return self.name

class RuleModel(BaseModel):
    __tablename__ = 'rule_model'

    name = Column(String(150), unique = True, nullable = False, default = '')
    amount = Column(Integer, default = 0)

class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User (BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    sex = Column(Boolean, default=True)
    date_of_birth = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.ADMIN)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name

class GoodReceived(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('GoodReceived_Detail', backref='goodreceipt', lazy=True)

    def __str__(self):
        return self.created_date

class GoodReceived_Detail(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    id_goodreceived = Column(Integer, ForeignKey(GoodReceived.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Book.id), nullable=False)

class Author(BaseModel):
    __tablename__ = 'author'
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name

class Receipt(BaseModel):
    __tablename__ = 'receipt'
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)

class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


        # r = Receipt(user_id = 1)
        # db.session.add(r)
        # db.session.commit()

        # r = ReceiptDetails(quantity=1, price = 50000, book_id = 1,receipt_id = 1 )
        # db.session.add(r)
        # db.session.commit()

        # import hashlib
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u = User(name='Nhân viên kho', username='nhanvienkho', password=password, user_role=UserRole.WAREHOUSE_MANGER,
        #          avatar='https://res.cloudinary.com/dcyzg2k36/image/upload/v1670940795/avatar_2_aceapm.jpg')
        # db.session.add(u)
        # db.session.commit()
        # c1 = book_author(book_id='1', author_id='1')
        # c2 = book_author(book_id='2', author_id='3')
        # c3 = book_author(book_id='3', author_id='2')
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()

        # p1 = Book(name='5 cm / s', description='Truyện tiểu thuyết', price=60000,
        #              image='https://res.cloudinary.com/dcyzg2k36/image/upload/v1670063031/9f486b740d4e4f24639fed732b3b1608_tn_alm3tp.jpg',
        #              category_id=3)
        # p2 = Book(name='Những đứa trẻ đuổi theo tinh tú', description='Truyện tiểu thuyết', price=80000,
        #              image='https://res.cloudinary.com/dcyzg2k36/image/upload/v1670061190/273e559ade0b7c46ab801821940ab5f6_k7sgnz.jpg',
        #              category_id=3)
        # p3 = Book(name='Apple Watch S5', description='Apple, 32GB', price=18000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=3)
        # p4 = Book(name='Galaxy Tab S8', description='Samsung, 128GB', price=22000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=2)
        # db.session.add_all([p1,p2])
        # db.session.commit()
