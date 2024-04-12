import sqlite3
# from dotenv import load_dotenv
# import os

from datetime import datetime

# load_dotenv()

DB = 'data.db'

connection = sqlite3.connect(DB)
sql = connection.cursor()


sql.execute(
    """
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    first_name TEXT,
    phone_number TEXT,
    reg_date DATETIME);
    """
)

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS products
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    desc TEXT,
    photo TEXT,
    video TEXT,
    price REAL,
    category TEXT,
    added_date DATETIME);
    """
)

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS cart
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_name TEXT,
    product_count INTEGER,
    total_price REAL);
    """
)

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS orders
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_name TEXT,
    product_count INTEGER,
    total_price REAL,
    order_date DATETIME);
    """
)

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS category
    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);
    """
)


sql.execute(
    """
CREATE TABLE IF NOT EXISTS location(
id INTEGER PRIMARY KEY AUTOINCREMENT, user_name INTEGER, latitude TEXT, longitude )

"""

)

def get_location(user_name, latitude, longitude):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()
    
    sql.execute("INSERT INTO location (user_name, latitude, longitude) VALUES (?,?,?)",
                (user_name, latitude,  longitude))
    
    
def register_user(telegram_id, first_name, phone_button):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    sql.execute(" INSERT INTO users (telegram_id, first_name, phone_number, reg_date) VALUES (?,?,?,?); ",
                (telegram_id, first_name, phone_button, datetime.now()))


    connection.commit()
    connection.close()


def check_user(telegram_id):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    user = sql.execute(" SELECT telegram_id FROM users WHERE telegram_id=?; ", (telegram_id,)).fetchone()

    if user:
        return True
    else:
        return False


def get_user_data(telegram_id):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    user = sql.execute(" SELECT first_name, phone_number FROM users WHERE telegram_id=?; ", (telegram_id,)).fetchone()

    if user:
        return user
    else:
        return False


def add_product(name, desc, photo, video, price, category):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    sql.execute(" INSERT INTO products (name, desc, photo, video, price, category, added_date) VALUES (?,?,?,?,?,?,?); ",
                (name, desc, photo, video, price, category, datetime.now()))

    connection.commit()
    connection.close()


def get_product_by_name(proudct_name):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    product = sql.execute(" SELECT * FROM products WHERE name=?; ", (proudct_name,))

    return product.fetchone()


def get_all_products():
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    all_products = sql.execute('SELECT name FROM products;').fetchall()

    products = [i[0] for i in all_products]

    return products


def get_products_by_category(category):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    products = sql.execute(" SELECT * FROM products WHERE category=?; ", (category,)).fetchall()

    all_products = [i[1] for i in products]

    return all_products


def delete_product(product_name):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    product_id = sql.execute(" SELECT id FROM products WHERE name=?; ", (product_name,)).fetchone()

    sql.execute(" DELETE FROM products WHERE id=?; ", (product_id[0],))

    connection.commit()
    connection.close()


def update_product_name(product_name, new_name):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    product_id = sql.execute(" SELECT id FROM products WHERE name=?; ", (product_name,)).fetchone()

    sql.execute(" UPDATE products SET name=? WHERE id=?; ", (new_name, product_id[0]))

    connection.commit()
    connection.close()


def update_product_desc(product_name, new_desc):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    product_id = sql.execute(" SELECT id FROM products WHERE name=?; ", (product_name,)).fetchone()

    sql.execute(" UPDATE products SET desc=? WHERE id=?; ", (new_desc, product_id[0]))

    connection.commit()
    connection.close()


def update_product_photo(product_name, new_photo):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    product_id = sql.execute(" SELECT id FROM products WHERE name=?; ", (product_name,)).fetchone()

    sql.execute(" UPDATE products SET photo=? WHERE id=?; ", (new_photo, product_id[0]))

    connection.commit()
    connection.close()


def update_product_video(product_name, new_video):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    product_id = sql.execute(" SELECT id FROM products WHERE name=?; ", (product_name,)).fetchone()

    sql.execute(" UPDATE products SET video=? WHERE id=?; ", (new_video, product_id[0]))

    connection.commit()
    connection.close()


def update_product_price(product_name, new_price):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    product_id = sql.execute(" SELECT id FROM products WHERE name=?; ", (product_name,)).fetchone()

    sql.execute(" UPDATE products SET price=? WHERE id=?; ", (new_price, product_id[0]))

    connection.commit()
    connection.close()


def update_product_category(product_name, new_category):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    product_id = sql.execute(" SELECT id FROM products WHERE name=?; ", (product_name,)).fetchone()

    sql.execute(" UPDATE products SET category=? WHERE id=?; ", (new_category, product_id[0]))

    connection.commit()
    connection.close()


def add_category(name):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    sql.execute(" INSERT INTO category (name) VALUES (?); ", (name,))

    connection.commit()
    connection.close()


def delete_category(name):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    sql.execute(" DELETE FROM category WHERE name=?; ", (name,))

    connection.commit()
    connection.close()


def get_all_categories():
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    all_categories = sql.execute('SELECT name FROM category;').fetchall()

    categories = [i[0] for i in all_categories]

    return categories


def add_product_to_cart(telegram_id, product_name, product_count):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    product_price = sql.execute('SELECT price FROM products WHERE name=?', (product_name,)).fetchone()

    total_price = product_price[0] * product_count

    sql.execute(" INSERT INTO cart (user_id, product_name, product_count, total_price) VALUES (?,?,?,?); ",
                (telegram_id, product_name, product_count, total_price))

    connection.commit()
    connection.close()


def get_user_cart(telegram_id):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    user_cart = sql.execute(" SELECT product_name, product_count, total_price FROM cart WHERE user_id=?; ", (telegram_id,)).fetchall()

    return user_cart


def clear_user_cart(telegram_id):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    sql.execute(" DELETE FROM cart WHERE user_id=?; ", (telegram_id,))

    connection.commit()
    connection.close()


def add_order(telegram_id, product_name, product_count, total_price):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    sql.execute(" INSERT INTO orders (user_id, product_name, product_count, total_price, order_date) VALUES (?,?,?,?,?); ",
                (telegram_id, product_name, product_count, total_price, datetime.now()))

    connection.commit()
    connection.close()


def get_user_orders(telegram_id):
    connection = sqlite3.connect(DB)
    sql = connection.cursor()

    user_order = sql.execute(" SELECT product_name, product_count, total_price FROM order WHERE user_id=?; ", (telegram_id,)).fetchall()

    if user_order:
        return user_order

    else:
        return False
