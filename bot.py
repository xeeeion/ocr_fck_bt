import cv2
import telebot
import pytesseract
import config_OCR
import os.path

from telebot import types

memory_init_size = 1000
bot = telebot.TeleBot(config_OCR.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    answer = 'Сначала загрузи фото, а потом нажми на кнопку слева'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    recognize = types.KeyboardButton("Распознаем")
    help  = types.KeyboardButton("Помощь")
    markup.add(recognize, help)

    bot.send_message(message.chat.id, answer.format(message.from_user, bot.get_me()), reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo = ', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID = ', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path = ', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('../ocr_bot/image.png','wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, 'Теперь жми')


@bot.message_handler(content_types=['text'])
def lang_select(message):
    if message.text == 'Распознаем':

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Русский', callback_data='rus'))
        markup.add(telebot.types.InlineKeyboardButton(text='English', callback_data='eng'))

        bot.send_message(message.chat.id, text='Выбери язык', reply_markup=markup)

    elif message.text == 'Помощь':
        answer = 'Привет!\n' \
                 'Я предназначен распознования текста на картинке\n' \
                 'Чтобы перевести изображение в формат текста просто сделай 4 шага:\n' \
                 '1. Загрузи картинку\n' \
                 '2. Нажми кнопку Распорзнаем\n' \
                 '3. Выбери язык\n' \
                 '4. Получи результат'
        bot.send_message(message.chat.id,answer)
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = ''
    if call.data == 'rus':
        img = cv2.imread('../ocr_bot/image.png')  # select lang rus
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        config = r'--oem 3 --psm 6'
        answer = (pytesseract.image_to_string(img,config=config,lang='rus'))
        print("done lang_setting")

    elif call.data == 'eng':
        img = cv2.imread('../ocr_bot/image.png')  # select lang en
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        config = r'--oem 3 --psm 6'
        answer = (pytesseract.image_to_string(img,config=config,lang='eng'))
        print("done lang_setting")

    bot.send_message(call.message.chat.id, answer)

bot.polling(none_stop=True)

