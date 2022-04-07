import telebot
from telebot import types
from random import choice
from time import sleep
bot = telebot.TeleBot('5202097813:AAGHfqeV3NSw-117EbbHfs650Jtu_ASbDU4')
def readAnswer(Number):
    file = open(r'Quests1-12.txt', mode='r', encoding='utf-8')
    Read = False
    Text = []
    for text in file:
        if not Read:
            print(text.strip().split('.;')[0])
            try:
                if text.strip().split('.;')[0] == Number:
                    Read = True
            except:
                pass
        else:
            print(text)
            try:
                if len(text.strip().split('.;')) > 1:
                    if text.strip().split('.;')[0] != Number:
                        Read = False
                        break
                else:
                    Text.append(text.strip())
            except:
                pass
    file.close()
    return Text
def readlist(file, kword):
    filetemp = f'{file}'
    List = []
    for num in open(file, mode='r', encoding='utf-8'):
        if num.strip().split(':')[0] == kword:
            List.append(num.strip().split(':')[1])
    open(file, mode='r', encoding='utf-8').close()
    return List

def whitelist(file, list, kword):
    file = open(file, mode='w', encoding='utf-8')
    for num in list:
        file.write(kword + ':' + num+'\n')
    file.close()

def sum_text_dict(list, sep=' ', counting=False):
    List = ''
    if counting:
        count = 1
        for num in list:
            List += f'{str(count)}: {num + sep}'
            count += 1
    else:
        for num in list:
            List += num + sep
    return List

def read_root(file, kword):
    file = open(file, mode='r', encoding='utf-8')
    for num in file:
        if num.strip().split(':')[0] == kword:
            if num.strip().split(':')[1] == 'True':
                root = True
            else:
                root = False
            file.close()
            return root

def white_root(filetxt, kword, root='False'):
    file = open(f'{filetxt}', mode='r', encoding='utf-8')
    Dict = dict()
    for num in file:
        Dict[num.strip().split(':')[0]] = num.strip().split(':')[1]
    file.close()
    file = open(f'{filetxt}', mode='w', encoding='utf-8')
    Dict[kword] = root
    for num in Dict:
        file.write(f'{num}:{Dict[num]}' + '\n')
    file.close()
    return Dict


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    button_help = types.InlineKeyboardButton(text='/help', callback_data='name_help')
    keyboard.add(button_help)
    bot.send_message(message.from_user.id, 'Я Тест бот, для ознакомление с командами, введите',
                     reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if not read_root('Root', 'quest_by_number'):
        help_list = readlist('Help', 'Help')
        quest_list = readlist('List_Quest', 'Quest')
        if call.data == 'name_help':
            keyboard = types.InlineKeyboardMarkup()
            for num in help_list:
                button = types.InlineKeyboardButton(text=sum_text_dict(num.split()[0:]),
                                                    callback_data=f'name_{num.split()[0][1:]}')
                keyboard.add(button)
            bot.send_message(call.message.chat.id, 'Команды:', reply_markup=keyboard)
        elif call.data == 'name_add_question':
            Keyboard = types.InlineKeyboardMarkup()
            Button = types.InlineKeyboardButton(text='По № вопроса', callback_data='name_quest_by_number')
            Keyboard.add(Button)
            Button = types.InlineKeyboardButton(text='Рандомный вопрос', callback_data='name_quest_random')
            Keyboard.add(Button)
            bot.send_sticker(call.message.chat.id,
                             'CAACAgIAAxkBAAIFJmJB1uIc2WkrwB99vp-fB9FEzW5zAAIJEQACgdCJS58JXvdE8PApIwQ')
            bot.send_message(call.message.chat.id, 'Как выбрать вопрос?', reply_markup=Keyboard)
        elif call.data == 'name_questions':
            bot.send_message(call.message.chat.id, 'Вопросы:\n' + sum_text_dict(quest_list, sep='\n', counting=True))
            Keyboard = types.InlineKeyboardMarkup()
            Button = types.InlineKeyboardButton(text='По № вопроса', callback_data='name_quest_by_number')
            Keyboard.add(Button)
            Button = types.InlineKeyboardButton(text='Рандомный вопрос', callback_data='name_quest_random')
            Keyboard.add(Button)
            bot.send_sticker(call.message.chat.id,
                             'CAACAgIAAxkBAAIFJmJB1uIc2WkrwB99vp-fB9FEzW5zAAIJEQACgdCJS58JXvdE8PApIwQ')
            bot.send_message(call.message.chat.id, 'Как выбрать вопрос?', reply_markup=Keyboard)


        elif call.data == 'name_exit':
            bot.send_message(call.message.chat.id, 'Эту команду надо вводить в чат. Сама кнопка не имеет важной функции')
        elif call.data == 'name_quest_random':
            rand = choice([num for num in range(len(quest_list))])
            bot.send_message(call.message.chat.id, quest_list[rand])
            for temp in readAnswer(str(rand + 1)):
                bot.send_message(call.message.chat.id, temp)
            Keyboard = types.InlineKeyboardMarkup()
            Button = types.InlineKeyboardButton(text='По № вопроса', callback_data='name_quest_by_number')
            Keyboard.add(Button)
            Button = types.InlineKeyboardButton(text='Рандомный вопрос', callback_data='name_quest_random')
            Keyboard.add(Button)
            bot.send_message(call.message.chat.id, 'Как выбрать вопрос?', reply_markup=Keyboard)

        elif call.data == 'name_quest_by_number':
            white_root('Root', 'quest_by_number', 'True')
            bot.send_message(call.message.chat.id, 'Выбирайте цифру')

@bot.message_handler(content_types=['text'])
def messages(message):
    help_list = readlist('Help', 'Help')
    quest_list = readlist('List_Quest', 'Quest')
    if message.text == '/help':
        keyboard = types.InlineKeyboardMarkup()
        for num in help_list:
            button = types.InlineKeyboardButton(text=sum_text_dict(num.split()[0:]),
                                                callback_data=f'name_{num.split()[0][1:]}')
            keyboard.add(button)
        bot.send_message(message.chat.id, 'Команды:', reply_markup=keyboard)
    elif read_root('Root', 'quest_by_number'):
        if message.text == '/exit':
            white_root('Root', 'quest_by_number')
        else:
            try:
                bot.send_message(message.chat.id, quest_list[int(message.text) - 1])
                for temp in readAnswer(str(message.text)):
                    bot.send_message(message.chat.id, temp)
            except ValueError:
                bot.send_message(message.chat.id, 'Надо вводить цифру.')
            except IndexError:
                bot.send_message(message.chat.id, 'Этот номер выходит за диапозон вопросов')
    print(read_root('Root', 'quest_by_number'))


bot.polling(non_stop=True, interval=0)
