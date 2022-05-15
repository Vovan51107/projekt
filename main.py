import sqlite3
import telebot

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('proekteko.db', check_same_thread=True)
        self.cursor = self.conn.cursor()
    
    def dbget(self, arg_name, arg_id):
        self.cursor.execute(f'SELECT "{arg_name}" FROM users WHERE user_id="{arg_id}"')
        result = self.cursor.fetchone()
        return result[0]
    def dbupdate(self, arg_name, arg_id, arg_content):
        self.cursor.execute(f"UPDATE users SET {arg_name} = {arg_content} WHERE user_id = {arg_id}")
        self.conn.commit()
    def dbreg(self, *arg_content):
        self.cursor.execute(f'INSERT INTO users VALUES (?,?,?)', (arg_content[0], arg_content[1], arg_content[2]))
        self.conn.commit()

db = Database()

