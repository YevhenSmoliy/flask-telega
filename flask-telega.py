import os

from flask import Flask, request

import telebot
import sqlite3
import time
import datetime
import sys

TOKEN = '811351588:AAFUmQym9_euPVZO6scbtBFhW8-_amjmUHg'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start', 'Start'])
def echo_msg(message):
    chat_id = message.chat.id  
    try:
        create_db(chat_id)
        bot.send_message(chat_id,
                            text='Hello!If you see this messsage its mean that you are new member!!!GRATS')
    except:
        bot.send_message(chat_id,
                            text='Hello!Nice too see you again. /add - if you wanna ad smth,/info - if you wanna see total minus,/last - to see last 5 inputs.......Version 0.3C)')

# bot start message
@bot.message_handler(commands=['add', 'Add'])
def echo_msg2(message):
    
    echo = bot.send_message(chat_id=message.chat.id,
                            text='so what you wanna add?')
    bot.register_next_step_handler(message=echo, callback=extract_msg)

@bot.message_handler(commands=['info'])
def info_message(message):
    table_str=str(message.chat.id)
    conn = sqlite3.connect(table_str+'.db')
    cursor=conn.cursor()
    cursor.execute("SELECT balance FROM Doroga1 ORDER BY balance DESC LIMIT 1")
    Full_value_bd = cursor.fetchall()
    Full_value = Full_value_bd[0]
    Full,=Full_value
    bot.send_message(message.chat.id, 'Total minus:' + str(Full))
    print(message.chat.id)


@bot.message_handler(commands=['last'])
def last_message(message):
    bot.send_message(message.chat.id, '5 last adds')
    table_str=str(message.chat.id)
    conn = sqlite3.connect(table_str+'.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doroga1 ORDER BY balance DESC LIMIT 5")
    last = cursor.fetchall()
    print(message.chat.id)
    for x in last:
        print(x)
        bot.send_message(message.chat.id, str(x))


def extract_msg(message):
    global Name  # be global to use it in another function
    msg = (message.text)
    print(msg)
    Name = msg
    echo = bot.send_message(message.chat.id, 'price?')
    bot.register_next_step_handler(message=echo, callback=price_d)
    # get first value=name,make it global


def price_d(message):
    table_str=str(message.chat.id)
    conn = sqlite3.connect(table_str+'.db')
    cursor = conn.cursor()
    msg2 = (message.text)
    print(msg2)
    price = float(msg2)
    
    # take 2 value Price and make it float for object and class
    cursor.execute("SELECT balance FROM Doroga1 ORDER BY balance DESC LIMIT 1")
    Full_value_bd = cursor.fetchall()
    Full_value = Full_value_bd[0]
    Full,=Full_value
    
    timec = datetime.datetime.now()
    cursor.execute("INSERT INTO Doroga1 VALUES(?,?,?,?)", (Name, price, add(Full,price), timec))
    conn.commit()
    bot.send_message(message.chat.id,
                     'You add: ' + str(Name) + '\n' + '.With price:' + msg2 + '\n' + " Total minus:" + str(
                         add(Full,price)))
    # add all creatind valuse in db,bot print valus for us,end


def create_db(id_user):
    id_user1=str(id_user)
    conn=sqlite3.connect(id_user1+".db")
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE Doroga1(type text, na_doroga real, balance real, date text)""")
    cursor.execute("INSERT INTO Doroga1 VALUES(?,?,?,?)", (0, 0, 0, 0))
    
    conn.commit()


def add(full,amount):
    all=full+amount
    return all


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://hashengard.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
