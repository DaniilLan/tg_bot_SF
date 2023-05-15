# -*- coding: cp1251 -*-

from extensions import Exchange, ExchangeException
from config import *
import telebot
from telebot import types

bot = telebot.TeleBot(token)


def message_info(message):
    user_name = message.from_user.username
    user_text = message.text
    print(f'{user_name}: {user_text}')


@bot.message_handler(commands=["Start"])
def button_commands(message):
    markup = types.ReplyKeyboardMarkup()
    command1 = types.KeyboardButton('Доступная валюта')
    command2 = types.KeyboardButton('Как конвертировать валюту')
    markup.add(command1, command2)
    bot.send_message(message.chat.id, "Привет, это бот для конвертации валют, воспользуйтесь кнопкой "
                                      "'Доступная валюта' или напишите сообщение 'Доступная валюта', что бы получть "
                                      "подробную информацию.", reply_markup=markup)
    message_info(message)


@bot.message_handler(content_types=["text"])
def func_ex(message):
    if message.text == 'Доступная валюта':
        text = (f"Доступная валюта для конвертации:"
                f"\n")
        for i in nac_ex.keys():
            text += f"\n{i} - {nac_ex[i]}"
        text += ("\n"
                 "\n"
                 "Что бы начать конвертацию валюты воспользуйтесь кнопкой "
                 "'Как конвертировать валюту'."
                 "\nИли напишите сообщение 'Как конвертировать валюту'")
        bot.reply_to(message, text)
    elif message.text == 'Как конвертировать валюту':
        text = ("Введите сообщение в формате:"
                "\n"
                "\n$ RUB EUR 50"
                "\n"
                "\nГде:"
                "\n'$' - знак конвертации"
                "\n'RUB' - переводимая валюта"
                "\n'EUR' - валюта в которую вы хотите перевести"
                "\n'50' - количество переводимой валюты")
        bot.reply_to(message, text)
    elif "$" in message.text:
        try:
            list_ex = message.text.split()
            if (len(list_ex) == 4) and (list_ex[0] == "$"):
                val1 = list_ex[1]
                val2 = list_ex[2]
                quantity = list_ex[3]
                value = Exchange.get_exchange(val1, val2, quantity)
                if float(value) < 0.0001:
                    value = '{:.8f}'.format(float(value)).rstrip('0').rstrip('.') # rstrip() генйи - кто придумал !
                    bot.reply_to(message, f"Цена {quantity} {val1.upper()} = {value} {val2.upper()}")
                else:
                    bot.reply_to(message, f"Цена {quantity} {val1.upper()} = {value} {val2.upper()}")
            else:
                text_error = ("Ошибка в написании команды конвертации валюты."
                              "\nПроверьте корректность введённой формы.")
                bot.reply_to(message, text_error)
        except ExchangeException as e:
            bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    else:
        bot.send_message(message.chat.id, "Напишите команду /Start для работы с ботом")
        message_info(message)


bot.polling()
