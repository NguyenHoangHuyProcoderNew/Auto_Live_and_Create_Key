import telebot

API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

user_id = "5634845912"

def bot_reply(user_id, message):
    # Gửi tin nhắn đến người dùng
    bot.send_message(user_id, message)  