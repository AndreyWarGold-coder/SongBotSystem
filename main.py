import telebot
import classes

mCommander = classes.CommandController()

API_TOKEN = '5168765423:AAHLNtr5AUTK5G5rd72pru7id3n4uJ8CveI'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['end'])
def gostart(message: telebot.types.Message):
    print("end")
    author = message.from_user.username
    author_id = message.from_user.id
    chat_id = str(message.chat.id)
    send_ReturnCommandObj(mCommander.end_session(chat_id, author, author_id, "telegram"), chat_id, None)
    print("end end")

@bot.message_handler(commands=['go'])
def gostart(message: telebot.types.Message):
    print("start_go")
    author = message.from_user.username
    author_id = message.from_user.id
    chat_id = str(message.chat.id)
    send_ReturnCommandObj(mCommander.start_defoult_mode(chat_id, author, "telegram"), chat_id, None)
    print("end_go")

@bot.callback_query_handler(lambda c: c.data.startswith("_skip"))
def skip_query(call: telebot.types.CallbackQuery):
    author = call.from_user.username
    author_id = call.from_user.id
    chat_id = str(call.message.chat.id)
    category = call.data.split("_")[1]
    bot.send_message(chat_id, "Нічого, наступного разу повезе!")
    send_ReturnCommandObj(mCommander.click_button(category, chat_id, author, author_id, "telegram"), chat_id, None)

@bot.callback_query_handler(lambda c: c.data.startswith("category_"))
def skip_query(call: telebot.types.CallbackQuery):
    author = call.from_user.username
    author_id = call.from_user.id
    chat_id = str(call.message.chat.id)
    category = call.data.split("_")[1]
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Обрана категорія " + category)
    send_ReturnCommandObj(mCommander.click_button(call.data, chat_id, author, author_id, "telegram"), chat_id, None)

def send_ReturnCommandObj(comm: classes.ReturnCommandObj, chat_id: str, message: telebot.types.Message):
    if( comm != None):
        print(comm.text, comm.replyText, comm.buttons, str(comm.file))
    if(comm != None):
        if(comm.text != None):
            if(comm.buttons != None and comm.file == None):
                markup = telebot.types.InlineKeyboardMarkup()
                for i in comm.buttons:
                    button = telebot.types.InlineKeyboardButton(i.split("_")[1], callback_data=i)
                    markup.add(button)
                bot.send_message(chat_id, comm.text, reply_markup=markup)
            else:
                bot.send_message(chat_id, comm.text)
        if(comm.replyText != None):
                bot.reply_to(message, comm.replyText)
        if(comm.file != None):
            if (comm.buttons != None):
                markup = telebot.types.InlineKeyboardMarkup()
                for i in comm.buttons:
                    button = telebot.types.InlineKeyboardButton(i.split("_")[1], callback_data=i)
                    markup.add(button)
                bot.send_audio(chat_id, comm.file.read(), reply_markup=markup)
            else:
                bot.send_audio(chat_id, comm.file.read())

@bot.message_handler(commands=['add'])
def gostart(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Ця функція тимчасово не працює, приносимо вибачення")
    return None
    #chat_id = str(message.chat.id)
    #text = message.text
    #text = text.split("/add ")[1]
    #text = text.split(" ")
    #if(len(text) > 3):
    #    bot.send_message(chat_id, "Ви ввели занадто багато аргументів! Ви впевненні, що ввели назву категорії без пробілів? Або ж у такому форматі /add <url> <name_category> <colvo>(optional) ")
    #    return
    #if(len(text) == 3):
    #    send_ReturnCommandObj(mCommander.download_playlist(text[0], text[1], int(text[2])), chat_id, None)
    #if(len(text) == 2):
    #    send_ReturnCommandObj(mCommander.download_playlist(text[0], text[1]), chat_id, None)

@bot.message_handler(content_types=['text'])
def gettext(message: telebot.types.Message):
    print("CommandTExt: " + message.text)
    text = message.text
    author = message.from_user.username
    author_id = message.from_user.id
    chat_id = str(message.chat.id)
    send_ReturnCommandObj(mCommander.command_text(text.lower(), chat_id, author, author_id, "telegram"), chat_id, message)



bot.infinity_polling()