"""Модуль для функций, предназначенных для работы исключительно с ботом"""
from telebot import types


def start(chat_id, bot):
    """Предлагает пользователю выбрать действие (выпить кофе)"""
    button1 = types.InlineKeyboardButton(text="Хочу выпить кофе!", callback_data="coffee")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    bot.send_message(chat_id, "Выберите действие 😄", reply_markup=markup)


def choose_department(message_chat_id, bot):
    """Предлагает пользователю выбрать офис"""
    button1 = types.InlineKeyboardButton(text="Большая морская 🌊", callback_data="big_morsk")
    button2 = types.InlineKeyboardButton(text="Малая морская 🌴", callback_data="small_morsk")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1, button2)
    bot.send_message(message_chat_id, "Выберите отдел: 🏬", reply_markup=markup)
