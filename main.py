import sqlite3
import telebot
from telebot import types
from random import randint
from time import sleep


class Database():
    def __init__(self):
        self.conn = sqlite3.connect('proekteko.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def dbget(self, arg_name, arg_id):
        self.cursor.execute(f'SELECT "{arg_name}" FROM users WHERE user_id="{arg_id}"')
        result = self.cursor.fetchone()
        return result[0]
    def dbgetdata(self, arg_name, arg_id):
        self.cursor.execute(f'SELECT "{arg_name}" FROM users WHERE user_id="{arg_id}"')
        result = self.cursor.fetchone()
        return result
    def dbupdate(self, arg_name, arg_id, arg_content):
        self.cursor.execute(f"UPDATE users SET {arg_name} = {arg_content} WHERE user_id = {arg_id}")
        self.conn.commit()
    def dbreg(self, *arg_content):
        self.cursor.execute(f'INSERT INTO users VALUES (?,?,?,?,?,?)', (arg_content[0], arg_content[1], arg_content[2], arg_content[3], arg_content[4], arg_content[5]))
        self.conn.commit()



db = Database()
bot = telebot.TeleBot("5358126269:AAGiVX4xe6_2x7IBdjODm3y61aG2JgiPx5I")
works_status = {'clean': True, 'mine': True, 'fac': True, 'office': True, 'taxi': True, 'truck': True, 'doc': True, 'Military': True, 'crime': True}
print('Бот включён')


@bot.message_handler(commands=["start"])
def start_message(message):
    data = db.dbgetdata('user_id', message.chat.id)
    if data is None:
        if message.from_user.username is None:
            db.dbreg(message.chat.id, message.from_user.first_name, 1000, 100, 100, 'House 1 lvl')
        else:
            db.dbreg(message.chat.id, message.from_user.username, 1000, 100, 100, 'House 1 lvl')
        name = db.dbget('username', message.chat.id)
        money = db.dbget('cash', message.chat.id)
        heal = db.dbget('heal_points', message.chat.id)
        stamina = db.dbget('stamina_points', message.chat.id)
        bot.send_message(message.chat.id, f'Поздравляю, {name}, вы успешно зарегестрированы! \nВы - бот, житель Ботбурга. Ваша цель - выжить как можно дольше и занять первое место в рейтинге ботов. \nВы имеете: \n -{money} ботлингов (Валюта Ботбурга) \n -{heal} очков здоровья \n -{stamina} очков усталости \n -Дом первого уровня \nПравила: \n Если количество очков усталости персонажа опустится до 0, персонаж начнёт постоянно терять очки здоровья. Если очки здоровья персонажа опустятся до 0, ваш персонаж умрёт, и игра закончится. \nДля ознокомления с командами напишите "/help" в чат')
    else:
       bot.send_message(message.chat.id, 'Регистрация отклонена, вы уже зарегистрированы')



@bot.message_handler(commands=["rules"])
def rules(message):
    bot.send_message(message.chat.id, 'Правила: \n Если количество очков усталости персонажа опустится до 0, персонаж начнёт постоянно терять очки здоровья. Если очки здоровья персонажа опустятся до 0, ваш персонаж умрёт, и игра закончится.')



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/start - Регистрация нового персонажа \n/rules - Правила игры \n/help - Помощь (вы её сейчас ввели) \n/work - Меню работы \n/sleep - сон, восстонавливает очки усталости \n/eat - еда, восстонавливает очки усталости (платно)')



@bot.message_handler(commands=['work'])
def work_choice(message):
    data = db.dbgetdata('user_id', message.chat.id)
    if data != None:
        start_keyboard = types.InlineKeyboardMarkup()
        cleaner = types.InlineKeyboardButton(text='Уборщик', callback_data='clean')
        doctor = types.InlineKeyboardButton(text='Врач', callback_data='doc')
        miner = types.InlineKeyboardButton(text='Шахтёр', callback_data='mine')
        trucker = types.InlineKeyboardButton(text='Водитель грузовика', callback_data='truck')
        office = types.InlineKeyboardButton(text='Офисный работник', callback_data='office')
        factory = types.InlineKeyboardButton(text='Заводской работник', callback_data='fac')
        #criminal = types.InlineKeyboardButton(text='Преступление', callback_data='crime')
        taxi = types.InlineKeyboardButton(text='Таксист', callback_data='taxi')
        military = types.InlineKeyboardButton(text='Военный', callback_data='Military')
        sent = 'Информация о работе:\nУборщик: Зарплата-1000 ботлингов, Потребление очков усталости-25, Шанс успеха-90%\nШахтёр: Зарплата-7000'
        start_keyboard.add(cleaner, miner, factory, office, taxi, trucker, doctor, military)
        bot.send_message(message.chat.id, sent, reply_markup=start_keyboard)

@bot.callback_query_handler(func=lambda c: c.data)
def answer_callback(callback):
    sent = bot.send_message(callback.message.chat.id, "Вы ушли на работу")
    if callback.data == "clean":
        bot.register_next_step_handler(sent, work(callback, 'Уборщик', 90, 1000, 'clean', 25))
    elif callback.data == "doc":
        bot.register_next_step_handler(sent, work(callback, 'Врач', 75, 7500, 'doc', 40))
    elif callback.data == "mine":
        bot.register_next_step_handler(sent, work(callback, 'Шахтёр', 60, 7000, 'mine', 40))
    elif callback.data == "truck":
        bot.register_next_step_handler(sent, work(callback, 'Водитель грузовика', 65, 2600, 'truck', 15))
    elif callback.data == "office":
        bot.register_next_step_handler(sent, work(callback, 'Офисный работник', 75, 3600, 'office', 20))
    elif callback.data == "fac":
        bot.register_next_step_handler(sent, work(callback, 'Заводской работник', 55, 3000, 'fac', 30))
    elif callback.data == "taxi":
        bot.register_next_step_handler(sent, work(callback, 'Таксист', 65, 2600, 'taxi', 15))
    elif callback.data == "Military":
        bot.register_next_step_handler(sent, work(callback, 'Военный', 45, 9600, 'Military', 35))
'''  elif callback.data == "crime":
        bot.register_next_step_handler(sent, YUY) ###'''


def work(callback, name, chance, money, code, stam):
    sleep(randint(2, 5))
    rand = randint(0, 100)
    if rand <= chance and works_status[code] == True:
        sta = db.dbget('stamina_points', callback.message.chat.id)
        sta = int(sta) - int(stam)
        db.dbupdate('stamina_points', callback.message.chat.id, sta)
        profit = db.dbget('cash', callback.message.chat.id)
        profit = int(profit) + int(money)
        db.dbupdate('cash', callback.message.chat.id, profit)
        bot.send_message(callback.message.chat.id, f'Вы успешно выполнили работу в должности "{name}", и заработали {money} ботлингов, потеряв {stam} очков усталости.')
    elif rand > chance:
        bot.send_message(callback.message.chat.id, f'Вам не повезло, на вашей смене произошло ЧП. Вы не получили зарплату, но потеряли {stam} очков усталости. Эта работа теперь недоступна на 2 дня.')
        works_status[name] = False
        sta = db.dbget('stamina_points', callback.message.chat.id)
        sta = int(sta) - int(stam)
        db.dbupdate('stamina_points', callback.message.chat.id, sta)
    elif works_status[code] == False:
        bot.send_message(callback.message.chat.id, 'Эта работа ещё не восстановилась после недавнего ЧП')
    #хп и стамина


@bot.message_handler(commands=[sleep])
def sleep(message):
    lvl = db.dbget('house', message.chat.id)




bot.infinity_polling()