# Импортируем sqlalchemy
import sqlalchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func

# Имортируем функцию create_tables из файла models.py
from models import create_tables, Publisher, Book, Shop, Sale, Stock, SessionContext

login = input('Введите логин: ')
password = input('Введите пароль: ')
database = input('Введите название базы данных: ')

# Создаем подключение к базе данных
DSN = f'postgresql://{login}:{password}@localhost:5432/{database}'
engine = sqlalchemy.create_engine(DSN)

# Создаем движок с подключением к базе данных
create_tables(engine)

# Создаем переменную session для управления сессиями
Session = sessionmaker(bind=engine)
session = Session()

# Вносим данные об издательствах
pub1 = Publisher(name="ЭКСМО")
pub2 = Publisher(name="АСТ")
pub3 = Publisher(name="Просвещение")
pub4 = Publisher(name="АЗБУКА-Аттикус")
pub5 = Publisher(name="Стандарт-Информ")
session.add_all([pub1, pub2, pub3, pub4, pub5])
session.commit()

# Вносим данные о книгах
b1 = Book(title='Благословение небожителей. Том 1', id_publisher=1)
b2 = Book(title='Гибель имерии. Российский урок', id_publisher=1)
b3 = Book(title='Граф Аверин. Колдун Российской империи', id_publisher=1)
b4 = Book(title='Наследие', id_publisher=2)
b5 = Book(title='Мой театр', id_publisher=2)
b6 = Book(title='Кто в списке у судьи?', id_publisher=2)
b7 = Book(title='Двенадцать стульев. Золотой теленок. Сборник', id_publisher=3)
b8 = Book(title='Приключения Эмиля из Лённеберги (сборник)', id_publisher=3)
b9 = Book(title='Мартин Иден', id_publisher=3)
b10 = Book(title='Куда приводят мечты', id_publisher=4)
b11 = Book(title='Безмолвная земля', id_publisher=4)
b12 = Book(title='Уйти, чтобы вернуться', id_publisher=4)
b13 = Book(
    title='Теория, расчет и проектирование измерительных устройств. Часть 3. Проектирование измерительных систем',
    id_publisher=5)
b14 = Book(title='Автоматизация инженерных расчетов в среде Mathcad', id_publisher=5)
b15 = Book(title='Национальный стандарт Российской Федерации. Менеджмент риска. Методы оценки риска', id_publisher=5)
session.add_all([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15])
session.commit()

# Вносим данные о магазинах
sh1 = Shop(name='Читай-Город')
sh2 = Shop(name='Библио-Глобус')
sh3 = Shop(name='Московский дом книги')
sh4 = Shop(name='Лабиринт')
sh5 = Shop(name='Республика')
session.add_all([sh1, sh2, sh3, sh4, sh5])
session.commit()

# Вносим данные о складских остатках
st1 = Stock(id_book=1, id_shop=1, count=15)
st2 = Stock(id_book=2, id_shop=1, count=7)
st3 = Stock(id_book=3, id_shop=1, count=23)
st4 = Stock(id_book=4, id_shop=5, count=1)
st5 = Stock(id_book=5, id_shop=5, count=14)
st6 = Stock(id_book=6, id_shop=5, count=100)
st7 = Stock(id_book=7, id_shop=2, count=18)
st8 = Stock(id_book=8, id_shop=2, count=9)
st9 = Stock(id_book=9, id_shop=2, count=3)
st10 = Stock(id_book=10, id_shop=3, count=2)
st11 = Stock(id_book=11, id_shop=3, count=7)
st12 = Stock(id_book=12, id_shop=3, count=25)
st13 = Stock(id_book=13, id_shop=4, count=14)
st14 = Stock(id_book=14, id_shop=4, count=10)
st15 = Stock(id_book=15, id_shop=4, count=50)
session.add_all([st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15])
session.commit()

# Вносим данные о продажах
sale1 = Sale(price='1250', date_sale='2024-02-01', id_stock=1, count=1)
sale2 = Sale(price='1000', date_sale='2024-02-02', id_stock=2, count=2)
sale3 = Sale(price='1100', date_sale='2024-02-01', id_stock=3, count=1)
sale4 = Sale(price='780', date_sale='2024-02-01', id_stock=4, count=1)
sale5 = Sale(price='585', date_sale='2024-02-01', id_stock=5, count=2)
sale6 = Sale(price='990', date_sale='2024-02-01', id_stock=6, count=1)
sale7 = Sale(price='1170', date_sale='2024-02-01', id_stock=7, count=2)
sale8 = Sale(price='900', date_sale='2024-02-01', id_stock=8, count=2)
sale9 = Sale(price='780', date_sale='2024-02-01', id_stock=9, count=3)
sale10 = Sale(price='690', date_sale='2024-02-01', id_stock=10, count=1)
sale11 = Sale(price='1000', date_sale='2024-02-01', id_stock=11, count=4)
sale12 = Sale(price='900', date_sale='2024-02-01', id_stock=12, count=12)
sale13 = Sale(price='455', date_sale='2024-02-01', id_stock=13, count=6)
sale14 = Sale(price='230', date_sale='2024-02-01', id_stock=14, count=3)
sale15 = Sale(price='199', date_sale='2024-02-01', id_stock=15, count=25)
session.add_all([sale1, sale2, sale3, sale4, sale5, sale6, sale7, sale8, sale9, sale10, sale11, sale12, sale13, sale14,
                 sale15])
session.commit()


# Создаем функцию поиска данных о продажах книг в магазинах по названию или ID издательства
def get_shops(res_):
    query = session.query(
        Book.title, Shop.name, Sale.price, Sale.date_sale,
    ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if res_.isdigit():
        query = query.filter(Publisher.id == res_).all()
    else:
        query = query.filter(Publisher.name == res_).all()
    print(f'Информация о продажах книг данного издательства в книжных магазинах: ')
    for title, name, price, date_sale in query:
        print(f'{title:<50} | {name:<20} | {price:<5} | {date_sale}')


if __name__ == "__main__":
    res_ = input('Введите ID или название издательства: ')
    get_shops(res_)

# Отключаемся от БД (закрываем сессию)
session.close()
