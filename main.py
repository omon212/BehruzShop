import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import database
import buttons

TOKEN = '6830535886:AAGI1IYi4Afm3WqLqVydUVzXcc9xaXNaPCc'
bot = telebot.TeleBot(TOKEN, threaded=False)

adminnn = 6983244704

@bot.message_handler(commands=['start'])
def start_message(message):

    user = database.check_user(message.from_user.id)
    if user:
        bot.send_message(message.from_user.id, f'Здраствуйте {message.from_user.first_name}, выберите пункт в меню', reply_markup=buttons.main_menu())

    else:
        bot.send_message(message.from_user.id, f'Здраствуйте {message.from_user.first_name}, что бы использовать бот, отправьте номер телефона с помощью кнопки ниже', reply_markup=buttons.contact_button())
        bot.register_next_step_handler(message, get_contact)


def get_contact(message):
    telegram_id = message.from_user.id

    if message.contact:
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name

        database.register_user(telegram_id, first_name, phone_number)

        bot.send_message(telegram_id, 'Вы успешно зарегистрировались, выберите пункт в меню', reply_markup=buttons.main_menu()) # menu button

    else:
        bot.send_message(message.from_user.id, 'Отправьте номер телефона используя кнопку "Отправить номер"', reply_markup=buttons.contact_button()) # phone_button
        bot.register_next_step_handler(message, get_contact)


@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == 6983244704:
        bot.send_message(message.from_user.id, 'Вы вошли в админ панель ⬅️', reply_markup=buttons.admin_menu())


def get_product_to_update(message):
    if message.text == 'Назад ⬅️':
        bot.send_message(message.from_user.id, 'Вы вернулись в админ панель', reply_markup=buttons.admin_menu())

    else:
        product = message.text
        bot.send_message(message.from_user.id, 'Выберите что хотите изминить', reply_markup=buttons.admin_update_buttons())
        bot.register_next_step_handler(message, get_admin_action, product)


def get_admin_action(message, product):
    action = message.text
    text = None

    if action == 'Изменить название':
        text = 'Отправьте новое название товара'

    elif action == 'Изменить описание':
        text = 'Отправьте новое описание товара'

    elif action == 'Изменить цену':
        text = 'Отправьте новое цену товара'

    elif action == 'Изменить категорию':
        text = 'Отправьте новое категорию товара'

    elif action == 'Изменить фото':
        text = 'Отправьте новое фото товара'

    elif action == 'Изменить видео':
        text = 'Отправьте новое видео товара'

    bot.send_message(message.from_user.id, text)
    bot.register_next_step_handler(message, get_new_data, product, action)


def get_new_data(message, product, action):
    new_data = None

    if message.text:
        new_data = message.text

    elif message.photo[-1].file_id != None:
        new_data = message.photo[-1].file_id

    elif message.video.file_id != None:
        new_data = message.video.file_id

    else:
        print('error')
        # bot.send_message(message.from_user.id, 'Invalid name for product')
        # bot.register_next_step_handler(message, get_admin_action, product, action)

    if action == 'Изменить название':
        database.update_product_name(product, new_data)
        bot.send_message(message.from_user.id, 'Название товара успешно изменено')

    elif action == 'Изменить описание':
        database.update_product_desc(product, new_data)
        bot.send_message(message.from_user.id, 'Описание товара успешно изменено')

    elif action == 'Изменить цену':
        database.update_product_price(product, new_data)
        bot.send_message(message.from_user.id, 'Цена товара успешно изменено')

    elif action == 'Изменить категорию':
        database.update_product_category(product, new_data)
        bot.send_message(message.from_user.id, 'Категория товара успешно изменено')

    elif action == 'Изменить фото':
        database.update_product_photo(product, new_data)
        bot.send_message(message.from_user.id, 'Фотография товара успешно изменено')

    elif action == 'Изменить видео':
        database.update_product_video(product, new_data)
        bot.send_message(message.from_user.id, 'Видео товара успешно изменено')


def get_product_name(message, action):
    name = message.text

    if action == 'удалить':

        database.delete_product(name)
        bot.send_message(message.from_user.id, 'Продукт успешно удаленo', reply_markup=buttons.admin_menu())

    elif action == 'добавить':
        bot.send_message(message.from_user.id, 'Введите описание товара')
        bot.register_next_step_handler(message, get_product_desc, name)


def get_product_desc(message, name):
    desc = message.text

    bot.send_message(message.from_user.id, 'Введите цену товара в суммах!')
    bot.register_next_step_handler(message, get_product_price, name, desc)


def get_product_price(message, name, desc):
    price = message.text

    bot.send_message(message.from_user.id, 'Выберите категорию товара', reply_markup=buttons.categories_button())
    bot.register_next_step_handler(message, get_product_category, name, desc, price)


def get_product_category(message, name, desc, price):
    category = message.text

    bot.send_message(message.from_user.id, 'Отправьте фото товора, если нет фотографии нажмите кнопку "Пропустить"', reply_markup=buttons.skip_button())
    bot.register_next_step_handler(message, get_product_photo, name, desc, price, category)


def get_product_photo(message, name, desc, price, category):
    photo = None

    if message.text or message.text == 'Пропустить':
        photo = 'Пропустить'

    elif message.photo:
        photo = message.photo[-1].file_id

    else:
        bot.send_message(message.from_user.id, 'Отправьте фото товора, если нет фотографии нажмите кнопку "Пропустить"', reply_markup=buttons.skip_button())
        bot.register_next_step_handler(message, get_product_photo, name, desc, price, category)

    bot.send_message(message.from_user.id, 'Отправьте видео товора, если нет видео нажмите кнопку "Пропустить"', reply_markup=buttons.skip_button())
    bot.register_next_step_handler(message, get_product_video, name, desc, price, category, photo)


def get_product_video(message, name, desc, price, category, photo):
    video = None

    if message.text or message.text == 'Пропустить':
        video = 'Пропустить'

    elif message.video:
        video = message.video.file_id

    else:
        bot.send_message(message.from_user.id, 'Отправьте видео товора, если нет видео нажмите кнопку "Пропустить"', reply_markup=buttons.skip_button())
        bot.register_next_step_handler(message, get_product_video, name, desc, price, category, photo)

    database.add_product(name=name, desc=desc, photo=photo, video=video, price=price, category=category)

    bot.send_message(message.from_user.id, 'Товар успешно добавлен', reply_markup=buttons.admin_menu())


def get_category_name(message, action):
    if action == 'добавить':
        name = message.text
        database.add_category(name)

        bot.send_message(message.from_user.id, 'Категория успешно добавлено', reply_markup=buttons.admin_menu())

    elif action == 'удалить':
        name = message.text
        database.delete_category(name)

        bot.send_message(message.from_user.id, 'Категория успешно удалено', reply_markup=buttons.admin_menu())



@bot.message_handler(content_types=["location"])
def handle_location(message):
    global latitude, longitude
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    bot.reply_to(message, "Лакация принята",)
    bot.send_message(message.from_user.id, "подтвердить товар", reply_markup=buttons.confirm_order_button())
    bot.register_next_step_handler(message, get_accept)
    


@bot.message_handler(content_types=['text'])
def text_messages(message):
    if message.text == "Забрать самому":
        bot.send_message(message.from_user.id, f' Перейдите по ссылке администратора бота. Администратор вышлет вам адрес и вы заберете свой товар.\n @{"BZA2010"}\n👆admin')
    elif message.text == "Яндекс доставка":
        bot.send_location(message.from_user.id, latitude, longitude)
        bot.send_message(message.from_user.id , f'Если вам нужна служба доставки \nОтправьте необходимую сумму на карту 9843727894327878 и отправьте чек администратору, администратор свяжется с вами в течение 1-2 часов после определения цены товара и суммы оплаченной вами оплаты. \n и мы доставим по указанному вами адресу. Доставка тоже платная.\n @{"BZA2010"}\n👆admin')
    elif message.text == 'назад':
        bot.send_message(message.from_user.id , "Вы в главном меню", reply_markup=buttons.main_menu())

    admin_id = 6983244704

    if message.from_user.id == admin_id or message.from_user.id == 6983244704:
        if message.text == 'Добавить товар':
            action = 'добавить'
            bot.send_message(admin_id, 'Введите название товара', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_product_name, action)

        elif message.text == 'Редактирировать товар':
            bot.send_message(admin_id, 'Выберите товар который хотите редактирировать', reply_markup=buttons.admin_pr_button())
            bot.register_next_step_handler(message, get_product_to_update)

        elif message.text == 'Удалить товар':
            action = 'удалить'
            bot.send_message(admin_id, 'Выберите товар который хотите удалить', reply_markup=buttons.admin_pr_button())
            bot.register_next_step_handler(message, get_product_name, action)

        elif message.text == 'Добавить категорию':
            action = 'добавить'
            bot.send_message(admin_id, 'Введите название категории', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_category_name, action)

        elif message.text == 'Удалить категорию':
            action = 'удалить'
            bot.send_message(admin_id, 'Выберите категорию которую хотите удалить', reply_markup=buttons.categories_button())
            bot.register_next_step_handler(message, get_category_name, action)

        # elif message.text == 'Назад':
        #     bot.send_message(admin_id, 'Вы вернулись в админ панель', reply_markup=buttons.admin_menu())


    if message.text == 'Категории одежды 🛍':
        bot.send_message(message.from_user.id, 'Выберите категорию 👇', reply_markup=buttons.categories_button())
        bot.register_next_step_handler(message, get_category)

    elif message.text == 'Корзина 🛒':
        user_cart = database.get_user_cart(message.from_user.id)

        # Формирование сообщения для вывода всей картины
        if user_cart:
            full_message = 'Ваша корзина:\n\n'

            for cart in user_cart:
                full_message += f'{cart[0]} : {cart[1]}шт : {cart[-1]} сум\n'

            bot.send_message(message.from_user.id, full_message, reply_markup=buttons.basket_button())

        else:
            bot.send_message(message.from_user.id, 'Корзина пустая')

    elif message.text == 'История покупок 🕒':
        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:
            full_message = 'Ваш заказы:\n\n'

            for cart in user_cart:
                full_message += f'{cart[0]} : {cart[1]}шт : {cart[-1]} сум\n'

            bot.send_message(message.from_user.id, full_message)

        else:
            bot.send_message(message.from_user.id, 'История заказов пустая')

    elif message.text == 'Консультация ☎️':
        bot.send_message(message.from_user.id, 'Наш контакт: +99890 017 89 98')

    elif message.text == 'Оформить заказ ✅':
        bot.send_message(message.from_user.id, 'Оформим заказ?', reply_markup=buttons.lacation_button())

    elif message.text == 'Очистить корзину ❌':
        bot.send_message(message.from_user.id, 'Вы точно хотите очистить корзину?', reply_markup=buttons.confirm_clear_button())
        bot.register_next_step_handler(message, get_accept)

    elif message.text == 'Основное меню ⬅️':
        bot.send_message(message.from_user.id, 'Вы вернулись основное меню ⬅️', reply_markup=buttons.main_menu())


def get_category(message):
    if message.text == 'Назад ⬅️':
        bot.send_message(message.from_user.id, 'Вы вернулись в основное меню ⬅️', reply_markup=buttons.main_menu())

    elif message.text == 'Корзина 🛒':
        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:
            full_message = 'Ваш заказы:\n\n'

            for cart in user_cart:
                full_message += f'{cart[0]} : {cart[1]}шт : {cart[-1]} сум\n'

            bot.send_message(message.from_user.id, full_message)

        else:
            bot.send_message(message.from_user.id, 'История заказов пустая')

    elif message.text in database.get_all_categories():
        category = message.text
        bot.send_message(message.from_user.id, f'Товары категории: {category}', reply_markup=buttons.get_ptoducts_by_category_button(category))
        bot.register_next_step_handler(message, product_name, category)

    else:
        bot.send_message(message.from_user.id, 'Выберите пункт из меню кнопок')
        bot.register_next_step_handler(message, get_category)


def product_name(message, category):

    if message.text == 'Назад ⬅️':
        bot.send_message(message.from_user.id, 'Вы вернулись назад в категории ⬅️', reply_markup=buttons.categories_button())
        bot.register_next_step_handler(message, get_category)

    elif message.text in database.get_all_products():
        user_product = message.text

        current_product = database.get_product_by_name(user_product)

        if current_product[3] != 'Пропустить':
            text = f'{current_product[1]}\n\n{current_product[2]}\n\nЦена: {current_product[5]} сум'

            bot.send_photo(message.from_user.id, photo=current_product[3], caption=text, reply_markup=buttons.add_to_cart_button())
            bot.register_next_step_handler(message, get_message, current_product[1], category)

        elif current_product[4] != 'Пропустить':
            text = f'{current_product[1]}\n\n{current_product[2]}\n\nЦена: {current_product[5]} сум'

            bot.send_video(message.from_user.id, video=current_product[4], caption=text, reply_markup=buttons.add_to_cart_button())
            bot.register_next_step_handler(message, get_message, current_product[1], category)


def get_message(message, pr_name, category):
    text = message.text
    if text == 'Назад ⬅️':
        bot.send_message(message.from_user.id, f'Вы вернулись назад в: {category}', reply_markup=buttons.get_ptoducts_by_category_button(category))
        bot.register_next_step_handler(message, product_name, category)

    elif text == 'Добавить в корзину 📥':
        bot.send_message(message.from_user.id, 'Введите количиство сколько штук хотите заказать')
        bot.register_next_step_handler(message, get_count, pr_name, category)

    else:
        bot.send_message(message.from_user.id, 'Введите только кол-во, например: 1')
        bot.register_next_step_handler(message, get_count, pr_name, category)


def get_count(message, pr_name, category):
    count = message.text

    if count == 'Назад ⬅️':
        bot.send_message(message.from_user.id, f'Вы вернулись назад в: {category}', reply_markup=buttons.get_ptoducts_by_category_button(category))
        bot.register_next_step_handler(message, product_name, category)

    elif count.isdigit():
        count = int(message.text)

        database.add_product_to_cart(message.from_user.id, pr_name, count)

        bot.send_message(message.from_user.id, 'Товар добавлен в корзину!', reply_markup=buttons.get_ptoducts_by_category_button(category))
        bot.register_next_step_handler(message, product_name, category)

    else:
        bot.send_message(message.from_user.id, 'Введите только кол-во, например: 1')
        bot.register_next_step_handler(message, get_count, pr_name, category)



def get_accept(message):
    user_id = message.from_user.id

    if message.text == 'Потвердить ✅':
        user_products = database.get_user_cart(user_id)
        user_data = database.get_user_data(user_id)

        full_order_message = 'Ваш заказ:\n\n'
        full_admin_message = f'Имя: {user_data[0]}\nНомер телефон: {user_data[1]}\n\n'
        total_sum = 0

        for order in user_products:
            # Для пользователя
            full_order_message += f'Товар: {order[0]} : {order[1]}шт : {order[-1]}сум\n'
            #  Для админа
            full_admin_message += f'{order[0]} : {order[1]}шт : {order[-1]}сум\n'
            # Подсчет общей суммы
            total_sum += order[-1]

        full_order_message += f'\nИтог: {total_sum} сум\n\nВаш заказ оформлен!'  # Для пользователя
        full_admin_message += f'\nИтог: {total_sum} сум'  # Для админа
        database.add_order(user_id, order[0], order[1], order[-1])
        bot.send_location(user_id, latitude, longitude)
        bot.send_message(user_id, full_order_message)
        bot.send_message(6983244704, full_admin_message)
        bot.send_location(6983244704, latitude, longitude)
        bot.send_message(6983244704, "По адресу")
  

        database.clear_user_cart(user_id)
        
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        btn_1 = KeyboardButton('Забрать самому')
        
        btn_2 = KeyboardButton('Яндекс доставка')
        btn_3 = KeyboardButton('назад')

        kb.row(btn_1, btn_2, btn_3)

        bot.send_message(message.from_user.id, "Вы забираете товар сами или вам нужна доставка?", reply_markup=kb)

    elif message.text == 'Да ✅.':
        database.clear_user_cart(message.from_user.id)
        bot.send_message(user_id, 'корзина очищена', reply_markup=buttons.main_menu())
    elif message.text == 'Нет ❌.':
        bot.send_message(user_id, 'Действие отменено', reply_markup=buttons.main_menu())
    

    else:
        bot.send_message(user_id, 'Заказ отменен', reply_markup=buttons.main_menu())
        
        


bot.polling()
