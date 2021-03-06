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
        self.cursor.execute(f'INSERT INTO users VALUES (?,?,?,?,?,?,?,?)', (arg_content[0], arg_content[1], arg_content[2], arg_content[3], arg_content[4], arg_content[5], arg_content[6], arg_content[7]))
        self.conn.commit()

    def dbdel(self, arg_id):
        self.cursor.execute(f'DELETE FROM users WHERE user_id={arg_id}')
        self.conn.commit()



db = Database()
bot = telebot.TeleBot("5358126269:AAGiVX4xe6_2x7IBdjODm3y61aG2JgiPx5I")
works_status = {'Уборщик': True, 'Шахтёр': True, 'Заводской работник': True, 'Офисный работник': True,
                'Таксист': True, 'Водитель грузовика': True, 'Врач': True, 'Военный': True, }
def keybode(texte):
    return types.InlineKeyboardButton(text=texte, callback_data=texte)
print('Бот включён')


@bot.message_handler(commands=["start"])
def start_message(message):
    data = db.dbgetdata('user_id', message.chat.id)
    if data is None:
        if message.from_user.username is None:
            db.dbreg(message.chat.id, message.from_user.first_name, 1000, 100, 100, 1, 1, 0)
        else:
            db.dbreg(message.chat.id, message.from_user.username, 1000, 100, 100, 1, 1, 0)
        name = db.dbget('username', message.chat.id)
        money = db.dbget('cash', message.chat.id)
        heal = db.dbget('heal_points', message.chat.id)
        stamina = db.dbget('stamina_points', message.chat.id)
        bot.send_message(message.chat.id, f'Поздравляю, {name}, вы успешно зарегестрированы! \nВы - бот, житель Ботбурга. Ваша цель - выжить как можно дольше и занять первое место в рейтинге ботов. \nВы имеете: \n -{money} ботлингов (Валюта Ботбурга) \n -{heal} очков здоровья \n -{stamina} очков усталости \n -Дом первого уровня \nПравила: \n Если количество очков усталости персонажа опустится до 0, персонаж начнёт постоянно терять очки здоровья. Если очки здоровья персонажа опустятся до 0, ваш персонаж умрёт, и игра закончится. \nДля ознокомления с командами напишите "/help" в чат')
    else:
        bot.send_message(
            message.chat.id, 'Регистрация отклонена, вы уже зарегистрированы (помощь - /help)')


@bot.message_handler(commands=["rules"])
def rules(message):
    bot.send_message(message.chat.id, 'Правила: \n Если количество очков усталости персонажа опустится до 0, персонаж начнёт постоянно терять очки здоровья. Если очки здоровья персонажа опустятся до 0, ваш персонаж умрёт, и игра закончится.')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/start - Регистрация нового персонажа \n/rules - Правила игры \n/help - Помощь (вы её сейчас ввели) \n/work - Меню работы \n/sleep - сон, восстанавливает очки усталости \n/eat - еда, восстонавливает очки усталости и очки здоровья (платно), в разработке \n/p или /passport - показывает информацию о вашем персонаже и его состояние (в том числе и баланс, кол-во очков здоровья и усталости')


@bot.message_handler(commands=['work'])
def work_choice(message):
    data = db.dbgetdata('user_id', message.chat.id)
    if data != None:
        start_keyboard = types.InlineKeyboardMarkup()
        sent = '*Информация о работе:*\n*Уборщик:* Зарплата-1000 ботлингов, Потребление очков усталости-25, Шанс успеха-90%\n*Шахтёр:* Зарплата-7000 ботлингов, Потребление очков усталости-40, Шанс успеха 60%\n*Заводской работник:* Зарплата-3000 ботлингов, Потребление очков усталости-30, Шанс успеха-55%\n*Офисный работник:* Зарплата-3600 ботлингов, Потребление очков усталости-20, Шанс успеха 75%\n*Таксист:* Зарплата-2600 ботлингов, Потребление очков усталости-15, Шанс успеха 65%\n*Водитель грузовика:* Зарплата-3500 ботлингов, Потребление очков усталости-25, Шанс успеха 65%\n*Врач:* Зарплата-7500 ботлингов, Потребление очков усталости-40, Шанс успеха 75%\n*Военный:* Зарплата-9600 ботлингов, Потребление очков усталости-35, Шанс успеха 45%\n*!!!После выбора работы, команду вводить дважды!!!*'
        start_keyboard.add(keybode('Уборщик'), keybode('Шахтёр'), keybode('Заводской работник'), keybode('Офисный работник'), keybode('Таксист'), keybode('Водитель грузовика'), keybode('Врач'), keybode('Военный'))
        bot.send_message(message.chat.id, sent, parse_mode= 'Markdown', reply_markup=start_keyboard)


@bot.callback_query_handler(func=lambda c: c.data)
def answer_callback(callback):
    sent = bot.send_message(callback.message.chat.id, "Вы ушли на работу")
    match callback.data:
        case None:
            pass
        case 'Уборщик':
            bot.register_next_step_handler(sent, work(callback, 'Уборщик', 90, 1000, 25))
        case 'Шахтёр':
            bot.register_next_step_handler(sent, work(callback, 'Шахтёр', 60, 7000, 40))
        case 'Заводской работник':
            bot.register_next_step_handler(sent, work(callback, 'Заводской работник', 55, 3000, 30))
        case 'Офисный работник':
            bot.register_next_step_handler(sent, work(callback, 'Офисный работник', 75, 3600, 20))
        case 'Таксист':
            bot.register_next_step_handler(sent, work(callback, 'Таксист', 65, 2600, 15))
        case 'Водитель грузовика':
            bot.register_next_step_handler(sent, work(callback, 'Водитель грузовика', 65, 2600, 15))
        case 'Врач':
            bot.register_next_step_handler(sent, work(callback, 'Врач', 75, 7500, 40))
        case 'Военный':
            bot.register_next_step_handler(sent, work(callback, 'Военный', 45, 9600, 35))




def work(callback, name, chance, money, stam):
    chance = int(chance)
    money = int(money)
    stam = int(stam)
    rand = randint(0, 100)
    sta = db.dbget('stamina_points', callback.message.chat.id)
    sta = int(sta)
    healp = db.dbget('heal_points', callback.message.chat.id)
    healp = int(healp)
    day = db.dbget('day_surv', callback.message.chat.id)
    day = int(day)
    if sta > 0 and healp > 0:
        if rand <= chance and works_status[name] == True:
            sta = sta - stam
            db.dbupdate('stamina_points', callback.message.chat.id, sta)
            profit = db.dbget('cash', callback.message.chat.id)
            profit = int(profit) + money
            db.dbupdate('cash', callback.message.chat.id, profit)
            bot.send_message(callback.message.chat.id,
                             f'Вы успешно выполнили работу в должности "{name}", и заработали {money} ботлингов, потеряв {stam} очков усталости.')
        elif rand > chance:
            bot.send_message(callback.message.chat.id,
                             f'Вам не повезло, на вашей смене произошло ЧП. Вы не получили зарплату, но потеряли {stam} очков усталости. Эта работа теперь недоступна на 2 дня.')
            works_status[name] = day
            sta = sta - stam
            db.dbupdate('stamina_points', callback.message.chat.id, sta)
        elif 2 > day - works_status[name]:
            bot.send_message(callback.message.chat.id,
                             'Эта работа ещё не восстановилась после недавнего ЧП')
    elif sta <= 0 and not healp <= 0:
        db.dbupdate('heal_points', callback.message.chat.id, int(healp) - 5)
        healp = db.dbget('heal_points', callback.message.chat.id)
        bot.send_message(callback.message.chat.id,
                         f'Вы слишком устали, отдохните пока ещё можете, работа подождёт (ваше здоровье - {healp})')
    elif healp <= 0:
        bot.send_message(callback.message.chat.id, f'Вы умерли прямо на работе.\nВы прожили {day} дней\n/start для начала новой игры')
        db.dbdel(callback.message.chat.id)


    # хп, еда, покупки (выплата долга)


@bot.message_handler(commands=['sleep'])
def sleep(message):
    day = db.dbget('day_surv', message.chat.id)
    day = int(day)
    lvl = db.dbget('house_lvl', message.chat.id)
    lvl = int(lvl)
    sta = db.dbget('stamina_points', message.chat.id)
    sta = int(sta)
    sta = sta + lvl * 20
    cash = db.dbget('cash', message.chat.id)
    cash = int(cash)
    healp = db.dbget('heal_points', message.chat.id)
    healp = int(healp)
    dolg = db.dbget('dolg_to_doc', message.chat.id)
    if healp <= 0:
        if lvl >= 2 and dolg == 0:
            bot.send_message(message.chat.id, f'Как только вы пришли домой, у вас резко заболело сердце (наверное, из-за недостатка сна). Вы успели вызвать скорую, вас спасли (Вы чуть не умерли на {day}-м дне жизни). Теперь вы должны больнице 1000 ботлингов. Коммуналку оплатил добрый сосед')
        elif dolg != 0:
            bot.send_message(message.chat.id, f'Как только вы пришли домой, у вас резко заболело сердце (наверное, из-за недостатка сна). Вы успели вызвать скорую, но из-за того что вы не выплатили долг больнице, алчные врачи Ботбурга решили не ехать к вам, поэтому вы не смогли спастись и умерли в одиночестве...\nВы прожили {day} дней\n/start для начала новой игры')
            db.dbdel(message.chat.id)
        elif lvl < 2:
            bot.send_message(message.chat.id, f'Как только вы пришли домой, у вас резко заболело сердце (наверное, из-за недостатка сна). В вашем районе не работает служба скорой помощи, поэтому вы не смогли спастись и умерли в одиночестве...\nВы прожили {day} дней\n/start для начала новой игры')
            db.dbdel(message.chat.id)
    else:
        if lvl == 1:
            money = 0
        elif cash >= money:
            money = cash - lvl * 100
        elif lvl != 1 and cash < money:

            bot.send.message(
                message.chat.id, 'Вам не хватило денег на коммуналку, вам пришлось продать свой дом и купить дом подешевле (коммуналка оплачена на сдачу)')
            money = 0
            lvl = lvl - 1
            db.dbupdate('house_lvl', message.chat.id, lvl)
            lvl = db.dbget('house_lvl', message.chat.id)
            lvl = int(lvl)
            sta = db.dbget('stamina_points', message.chat.id)
            sta = int(sta)
            sta = sta + lvl * 20
            db.dbupdate('stamina_points', message.chat.id, sta)
            day = db.dbget('day_surv', message.chat.id)
            day = day + 1
            db.dbupdate('day_surv', message.chat.id, day)
            db.dbupdate('cash', message.chat.id, money)
            bot.send_message(message.chat.id, f'Вы поспали в своём доме {lvl}-го уровня и восстановили {lvl * 20} очков усталости и потратили {money} ботлингов на коммуналку\nСегодня - {day}-й день вашего выживания.')
        if sta + sta < 100:
            db.dbupdate('stamina_points', message.chat.id, sta)
            day = db.dbget('day_surv', message.chat.id)
            day = int(day)
            day = day + 1
            db.dbupdate('day_surv', message.chat.id, day)
            db.dbupdate('cash', message.chat.id, money)
            bot.send_message(
                message.chat.id, f'Вы поспали в своём доме {lvl}-го уровня и восстановили {lvl * 20} очков усталости и потратили {money} ботлингов на коммуналку\nСегодня - {day}-й день вашего выживания.')
        else:
            db.dbupdate('stamina_points', message.chat.id, 100)
            day = db.dbget('day_surv', message.chat.id)
            day = int(day)
            day = day + 1
            db.dbupdate('day_surv', message.chat.id, day)
            bot.send_message(
                message.chat.id, f'Вы поспали в своём доме {lvl}-го уровня но не восстановили очки усталости, из-за того, что вы не успели устать, но тем не менее вы потратили {money} ботлингов на коммуналку\nСегодня - {day}-й день вашего выживания.')


@bot.message_handler(commands=['p', 'passport'])
def passport(message):
    uname = db.dbget('username', message.chat.id)
    ucash = db.dbget('cash', message.chat.id)
    uhp = db.dbget('heal_points', message.chat.id)
    usta = db.dbget('stamina_points', message.chat.id)
    uday = db.dbget('day_surv', message.chat.id)
    uhouse = db.dbget('house_lvl', message.chat.id)
    udolg = db.dbget('dolg_to_doc', message.chat.id)
    bot.send_message(message.chat.id, text=f'*Ваша статистика, {uname}:*\n*Баланс:* *{ucash}* ботлингов\n*Уровень дома:* *{uhouse}*\n*Ваше здоровье:* *{uhp}* очков здоровья\n*Ваша усталость:* *{usta}* очков усталости\n*Вы выжили:* *{uday}* дней\n*В сумме вы должны:* *{udolg}* ботлингов\nХороший результат, но у гигачада лучше.', parse_mode='Markdown')



bot.infinity_polling()

# 30.05 23:39