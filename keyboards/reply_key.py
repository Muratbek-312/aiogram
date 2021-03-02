from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton('Да')
btn2 = KeyboardButton('Нет')
keyboard = ReplyKeyboardMarkup(one_time_keyboard=True).row(btn1, btn2)

key_group = ReplyKeyboardMarkup(one_time_keyboard=True)
bt = KeyboardButton('Python vol. 9')
bt1 = KeyboardButton('Python vol. 10')
bt2 = KeyboardButton('Python-9. Even')
bt4 = KeyboardButton('Python-10. Even')
bt5 = KeyboardButton('JavaScript vol. 9')
bt6 = KeyboardButton('JavaScript vol. 10')
key_group.row(bt1, bt4)
key_group.row(bt, bt2)
key_group.row(bt5, bt6)