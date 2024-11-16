import telebot
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

API_TOKEN = '8047776117:AAHbhIHrp_qY1egwP1_LZrMG4oTILDsRF9I'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

# Список для хранения победителей
winners = []
prizes = ["prize1.png", "prize2.png", "prize3.png"]  # Призовые картинки


@bot.message_handler(commands=['start'])
def start_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение пользователю с кнопкой "Получить приз".
    """
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("Получить приз", callback_data="get_prize")
    markup.add(button)

    bot.send_message(message.chat.id, "👋 Привет! Нажми на кнопку, чтобы получить приз!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "get_prize")
def callback_query(call: telebot.types.CallbackQuery):
    user_id = call.message.chat.id

    try:
        # Проверяем, сколько победителей уже получили приз
        if len(winners) < 3:
            # Если победителей меньше 3, добавляем текущего пользователя
            if user_id not in winners:
                winners.append(user_id)
                # Выбираем приз для пользователя
                prize_img = prizes[len(winners) - 1]  # Приз для победителя по порядку

                # Отправляем картинку приза
                with open(f'img/{prize_img}', 'rb') as photo:
                    bot.send_photo(user_id, photo, caption="Поздравляем! Ты получил приз!")
                bot.answer_callback_query(call.id, "Поздравляем! Ты получишь приз!")

                logging.info(f"Пользователь {user_id} получил приз!")
            else:
                bot.send_message(user_id, "Ты уже получил приз!")
                bot.answer_callback_query(call.id, "Ты уже получил приз!")
        else:
            bot.send_message(user_id, "К сожалению, все призы уже разданы. Попробуй в следующий раз!")
            bot.answer_callback_query(call.id, "Призы закончились!")
            logging.info(f"Все призы уже разданы. Пользователь {user_id} не получил приз.")
    except Exception as e:
        bot.answer_callback_query(call.id, "Произошла ошибка. Попробуйте снова.")
        logging.error(f"Ошибка при обработке нажатия кнопки: {e}")


# Обработчик для команды /rating, который отображает рейтинг пользователей по призам
@bot.message_handler(commands=['rating'])
def handle_rating(message: telebot.types.Message):
    if winners:
        res = [f'| @{user_id:<11} | 1 приз    |' for user_id in winners]
        res = '\n'.join(res)
        res = f'|USER_ID      |COUNT_PRIZE|\n{"_"*26}\n' + res
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, "Пока нет победителей.")


@bot.message_handler(commands=['help'])
def help_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /help.
    Предоставляет информацию о помощи.
    """
    bot.send_message(message.chat.id, "❓ Если у вас возникли вопросы, пожалуйста, свяжитесь с поддержкой.\n"
                                      "💬 Мы всегда рады помочь!\n"
                                      "📧 Напишите на нашу почту: support@example.com")


@bot.message_handler(commands=['about'])
def about_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /about.
    Информация о боте.
    """
    bot.send_message(message.chat.id, "🤖 Этот бот создан для управления проектами.\n"
                                      "🌟 Он поможет вам отслеживать ваши работы и делиться ими с другими!\n"
                                      "🚀 Разработан с любовью для пользователей!")


@bot.message_handler(commands=['contact'])
def contact_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /contact.
    Предоставляет информацию для связи.
    """
    bot.send_message(message.chat.id, "📞 Свяжитесь с нами через:\n"
                                      "✉️ Email: support@example.com\n"
                                      "💬 Telegram: @support_bot\n"
                                      "📱 Или просто напишите в чат!")


@bot.message_handler(func=lambda message: True)
def echo_message(message: telebot.types.Message):
    """
    Обработчик для всех остальных сообщений.
    Отправляет обратно то, что пользователь написал.
    """
    bot.send_message(message.chat.id, "🗨️ Вы написали: " + message.text + "\n"
                                                                          "🤔 Если у вас есть вопросы, напишите /help!")


if __name__ == '__main__':
    bot.polling(none_stop=True)
