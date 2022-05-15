import sqlite3
import telebot


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
        bot.send_message(message.chat.id, f'Поздравляю, {name}, вы успешно зарегестрированы! \nВы - бот, житель Ботбурга. Ваша цель - выжить как можно дольше и занять первое место в рейтинге ботов. \nВы имеете: \n -{money} рублей \n -{heal} очков здоровья \n -{stamina} очков усталости \n-Дом первого уровня \nПравила: \n Если количество очков усталости персонажа опустится до 0, персонаж начнёт постоянно терять очки здоровья. Если очки здоровья персонажа опустятся до 0, ваш персонаж умрёт, и игра закончится. \nДля ознокомления с командами напишите "/help" в чат')
    else:
       bot.send_message(message.chat.id, 'Регистрация отклонена, вы уже зарегистрированы')



@bot.message_handler(commands=["rules"])
def rules(message):
    bot.send_message(message.chat.id, 'Правила: \n Если количество очков усталости персонажа опустится до 0, персонаж начнёт постоянно терять очки здоровья. Если очки здоровья персонажа опустятся до 0, ваш персонаж умрёт, и игра закончится.')



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/start - Регистрация нового персонажа \n/rules - Правила игры \n/help - Помощь (вы её сейчас ввели) \n')



@bot.message_handler(commands=[''])
def wpass(message):
    pass


bot.infinity_polling()