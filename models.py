# Импортируем sqlalchemy
import sqlalchemy as sq

from sqlalchemy.orm import DeclarativeBase, relationship


# Определяем класс Base (комм. теперь вроде так верно, начиная с версии SQLAlchemy 2.0 - вместо присвоения переменной)
class Base(DeclarativeBase):
    pass


# Создаем классы (таблицы)
class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True)

    def __str__(self):
        return f'Publisher {self.id}: ({self.name})'


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref='books')

    def __str__(self):
        return f'Book {self.id}: ({self.title}, {self.id_publisher})'


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)

    def __str__(self):
        return f'Shop {self.id}: ({self.name})'


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")

    def __str__(self):
        return f'Book {Stock.id}: ({self.id_book}, {self.id_shop}, {self.count})'


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sales")

    def __str__(self):
        return f'Sale {self.id}: ({self.price}, {self.date_sale}, {self.id_stock}, {self.count})'


# Создаем функцию создания таблиц из классов
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
