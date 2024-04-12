from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import database

def contact_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    button = KeyboardButton('Отправить номер ☎️', request_contact=True)
    kb.add(button)

    return kb


def lacation_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    button = KeyboardButton('Отправить локацию', request_location=True)
    kb.add(button)

    return kb


def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button1 = KeyboardButton('Категории одежды 🛍')
    button2 = KeyboardButton('Корзина 🛒')
    button3 = KeyboardButton('История покупок 🕒')
    button4 = KeyboardButton('Консультация ☎️')

    kb.row(button1)
    kb.add(button2, button3, button4)

    return kb


def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button1 = KeyboardButton('Добавить товар')
    button2 = KeyboardButton('Редактирировать товар')
    button3 = KeyboardButton('Удалить товар')
    button4 = KeyboardButton('Добавить категорию')
    button5 = KeyboardButton('Удалить категорию')

    kb.add(button1, button4, button3, button5, button2)

    return kb


def admin_update_buttons():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button1 = KeyboardButton('Изменить название')
    button2 = KeyboardButton('Изменить описание')
    button3 = KeyboardButton('Изменить цену')
    button4 = KeyboardButton('Изменить категорию')
    button5 = KeyboardButton('Изменить фото')
    button6 = KeyboardButton('Изменить видео')
    button7 = KeyboardButton('Назад ⬅️')

    kb.add(button1, button2, button3, button4, button5, button6, button7)

    return kb


def admin_pr_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    products = database.get_all_products()

    for i in products:
        kb.add(i)

    kb.row(KeyboardButton('Назад ⬅️'))

    return kb


def categories_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    categories = database.get_all_categories()
    main = KeyboardButton('Назад ⬅️')
    basket = KeyboardButton('Корзина 🛒')
    kb.add(main, basket)

    for i in categories:
        kb.add(KeyboardButton(str(i)))

    kb.row(KeyboardButton('Назад ⬅️'))

    return kb


def get_ptoducts_by_category_button(name):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    products = database.get_products_by_category(name)
    main = KeyboardButton('Назад ⬅️')
    basket = KeyboardButton('Корзина 🛒')
    kb.add(main, basket)

    for i in products:
        kb.add(KeyboardButton(str(i)))

    kb.row(KeyboardButton('Назад ⬅️'))

    return kb


def skip_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    btn = KeyboardButton('Пропустить')
    kb.add(btn)

    return kb


def add_to_cart_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    btn = KeyboardButton('Добавить в корзину 📥')
    btn2 = KeyboardButton('Назад ⬅️')
    kb.add(btn, btn2)

    return kb


# Кнопки корзины
def basket_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    order = KeyboardButton('Оформить заказ ✅')
    delete_cart = KeyboardButton('Очистить корзину ❌')
    back = KeyboardButton('Назад ⬅️')

    kb.add(order, delete_cart, back)

    return kb


# Оформление заказа
def confirm_order_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    confirm = KeyboardButton('Потвердить ✅')
    cancel = KeyboardButton('Отменить ❌')

    kb.row(cancel, confirm)

    return kb


def confirm_clear_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    confirm = KeyboardButton('Да ✅')
    cancel = KeyboardButton('Нет ❌')

    kb.row(cancel, confirm)

    return kb

