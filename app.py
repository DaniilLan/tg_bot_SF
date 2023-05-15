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
    command1 = types.KeyboardButton('��������� ������')
    command2 = types.KeyboardButton('��� �������������� ������')
    markup.add(command1, command2)
    bot.send_message(message.chat.id, "������, ��� ��� ��� ����������� �����, �������������� ������� "
                                      "'��������� ������' ��� �������� ��������� '��������� ������', ��� �� ������� "
                                      "��������� ����������.", reply_markup=markup)
    message_info(message)


@bot.message_handler(content_types=["text"])
def func_ex(message):
    if message.text == '��������� ������':
        text = (f"��������� ������ ��� �����������:"
                f"\n")
        for i in nac_ex.keys():
            text += f"\n{i} - {nac_ex[i]}"
        text += ("\n"
                 "\n"
                 "��� �� ������ ����������� ������ �������������� ������� "
                 "'��� �������������� ������'."
                 "\n��� �������� ��������� '��� �������������� ������'")
        bot.reply_to(message, text)
    elif message.text == '��� �������������� ������':
        text = ("������� ��������� � �������:"
                "\n"
                "\n$ RUB EUR 50"
                "\n"
                "\n���:"
                "\n'$' - ���� �����������"
                "\n'RUB' - ����������� ������"
                "\n'EUR' - ������ � ������� �� ������ ���������"
                "\n'50' - ���������� ����������� ������")
        bot.reply_to(message, text)
    elif "$" in message.text:
        try:
            list_ex = message.text.split()
            if (len(list_ex) == 4) and (list_ex[0] == "$"):
                val1 = list_ex[1]
                val2 = list_ex[2]
                quantity = list_ex[3]
                value = Exchange.get_exchange(val1, val2, quantity)
                bot.reply_to(message, f"���� {quantity} {val1.upper()} = {value} {val2.upper()}")
            else:
                text_error = ("������ � ��������� ������� ����������� ������."
                              "\n��������� ������������ �������� �����.")
                bot.reply_to(message, text_error)
        except ExchangeException as e:
            bot.reply_to(message, f'������ ������������.\n{e}')

    else:
        bot.send_message(message.chat.id, "�������� ������� /Start ��� ������ � �����")
        message_info(message)


bot.polling()
