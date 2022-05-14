import sqlite3
import telebot
import sqlite3

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('proekteko.db', check_same_thread=True)
        self.cursor = self.conn.cursor()
    
    def dbget(self, arg_name, arg_id):
        self.cursor.execute(f'SELECT "{arg_name}" FROM users WHERE user_id="{arg_id}"')
        result = self.cursor.fetchall()
        return result[0][0]
    def dbupgrade(self, arg_name, arg_id, arg_content):
        self.cursor.execute(f"UPDATE users SET {arg_name} = {arg_content} WHERE userID = {arg_id}")

db = Database()

print(db.dbget('cash', 99889896))

