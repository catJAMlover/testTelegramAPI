from threading import Thread
import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, types


CHANNEL_ID = 
CHANNEL_ID_SEC = 

app = Client(
    "test_app",
    api_id=,
    api_hash=''
)

bot = telebot.TeleBot('')

inline_keyboard = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text="Да", callback_data='yes_button')
btn2 = InlineKeyboardButton(text="Нет", callback_data='no_button')
inline_keyboard.row(btn1, btn2)


def bot_loop(bot):
    bot.infinity_polling()


def split_str_id(string):
    pointer = string.find('"forward_from_message_id":')
    substring = string[pointer + 27:]
    pointer = substring.find(',')
    return substring[0:pointer]


def split_str_emoji(string):
    pointer = string.find('"emoji":')
    substring = string[pointer + 9:]
    pointer = substring.find(',')
    return substring[0:pointer]


@app.on_message()
def new(client: Client, message: types.Message):
    if (message.chat.id != CHANNEL_ID) and (message.chat.id != CHANNEL_ID_SEC):
        return

    if message.chat.id == CHANNEL_ID:
        print("\nПолучено новое сообщение с ID:", message.id)
        print("Текст:", message.text)
        print("Дата:", message.date)
        bot.edit_message_reply_markup(CHANNEL_ID, message.id, reply_markup=inline_keyboard)

    if message.chat.id == CHANNEL_ID_SEC and message.reply_to_message_id != None:
        print("\nПолучен новый ответ с ID:", message.id)
        print("Ответ на сообщение с ID:", split_str_id(str(message.reply_to_message)))
        print("Текст:", message.text)
        print("Дата:", message.date)
        print('От пользователя с ID:', message.from_user.id)
        print('От пользователя:', message.from_user.first_name)


@app.on_edited_message()
def edit(client: Client, message: types.Message):
    if message.chat.id != CHANNEL_ID:
        return

    if message.reactions is not None:
        print("\nИзменено сообщение с ID:", message.id)
        print("Получена реакция:", split_str_emoji(str(message.reactions)))
        print("Дата:", message.date)
        print('От пользователя:', message.from_user.first_name)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'yes_button':
        print('\nПользователь с ID:', call.from_user.id, '\nДал ответ: "Да" \nНа сообщение с ID:',
              call.message.message_id)
        print('От пользователя:', call.from_user.first_name)
        bot.edit_message_text(call.message.text + "\nОтвет: Да" + "\nOт пользователя: " + call.from_user.first_name,
                              CHANNEL_ID, call.message.message_id, reply_markup=None)
        print("Дата:", datetime.datetime.now().replace(microsecond=0))

    if call.data == 'no_button':
        print('\nПользователь с ID:', call.from_user.id, '\nДал ответ: "Нет" \nНа сообщение с ID:',
              call.message.message_id)
        print('От пользователя:', call.from_user.first_name)
        bot.edit_message_text(call.message.text + "\nОтвет: Нет" + "\nOт пользователя: " + call.from_user.first_name,
                              CHANNEL_ID, call.message.message_id, reply_markup=None)
        print("Дата:", datetime.datetime.utcnow().replace(microsecond=0))

# @app.on_raw_update()
# async def raw(client, update, users, chats, message):
#     if message.chat.id == CHANNEL_ID or message.chat.id == CHANNEL_ID_SEC:
#         print(update)

if __name__ == '__main__':
    Thread(target=bot_loop, args=(bot,)).start()
    app.run()
