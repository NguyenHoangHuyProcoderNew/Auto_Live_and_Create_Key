# IMPORT CÁC THƯ VIỆN CẦN THIẾT
import os
import time
import logging
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import telebot
import sys
from selenium.common.exceptions import NoSuchElementException
import datetime
from telebot import types

# Nhập moudles in log ra màn hình
from Moudles_support.print_log import log_info, log_warning, log_error, log_success

# Nhập moudles bot phản hồi lại người dùng
from Moudles_support.support_bot import bot_reply

# KHAI BÁO API TOKEN BOT TELEGRAM
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

"""" Bắt đầu các chức năng của bot """
log_success(f"KHỞI ĐỘNG BOT LIVESTREAM THÀNH CÔNG - ĐANG CHỜ LỆNH TỪ NGƯỜI DÙNG...") 

# Chức năng /start
@bot.message_handler(commands=['start'])
def chucnang_start(message):
    nut_start = telebot.types.ReplyKeyboardMarkup(True)
    nut_start.add("Mở live").add("Tắt live").add("Đổi IP")
    bot.send_message(message.chat.id, "Chào mừng bạn quay lại bot, chúc bạn ngày mới vui vẻ", reply_markup=nut_start)
    log_success("Người dùng đã sử dụng lệnh /start")

# Chức năng mở live
@bot.message_handler(func=lambda message: message.text == "Mở live")
def chon_taikhoan_molive(message):
    nut_chontaikhoan_molive = types.ReplyKeyboardMarkup(True).add('Mở live tài khoản Chính LBH').add('Mở live tài khoản Meme').add('Mở live tài khoản Bảo Hân Store').add('Trở lại menu chính')
    bot.send_message(message.chat.id, "Vui lòng chọn tài khoản cần mở live", reply_markup=nut_chontaikhoan_molive)
    log_info(f"Người dùng đã chọn Mở live từ menu chính, đang yêu cầu người dùng chọn tài khoản cần mở live")

# # Mở live tài khoản Tấn Tài
# @bot.message_handler(func=lambda message: message.text == "Mở live tài khoản Tấn Tài")
# def molive_vanbao(message):
#     from Moudles_live.Molive_TanTai import chon_nguon_chophienlive_tantai, xuly_molive_tantai
#     chon_nguon_chophienlive_tantai(message)
#     bot.register_next_step_handler(message, xuly_molive_tantai)

#     log_info("Người dùng đã chọn mở live tài khoản Tấn Tài")

# # Mở live tài khoản phụ LBH
# @bot.message_handler(func=lambda message: message.text == "Mở live tài khoản phụ LBH")
# def molive_phulbh(message):
#     from Moudles_live.Molive_PhuLBH import chon_nguon_chophienlive_phulbh, xuly_molive_phulbh
#     chon_nguon_chophienlive_phulbh(message)
#     bot.register_next_step_handler(message, xuly_molive_phulbh)

#     log_info("Người dùng đã chọn mở live tài khoản phụ LBH")

# Mở live tài khoản Meme
@bot.message_handler(func=lambda message: message.text == "Mở live tài khoản Meme")
def molive_meme(message):
    from Moudles_live.Molive_Meme import chon_nguon_chophienlive_meme, xuly_molive_meme
    chon_nguon_chophienlive_meme(message)
    bot.register_next_step_handler(message, xuly_molive_meme)

    log_info("Người dùng đã chọn mở live tài khoản Meme")

# Mở live tài khoản Bảo Hân Store
@bot.message_handler(func=lambda message: message.text == "Mở live tài khoản Bảo Hân Store")
def molive_baohanstore(message):
    from Moudles_live.Molive_BaoHanStore import chon_nguon_chophienlive_baohanstore, xuly_molive_baohanstore
    chon_nguon_chophienlive_baohanstore(message)
    bot.register_next_step_handler(message, xuly_molive_baohanstore)

    log_info("Người dùng đã chọn mở live tài khoản Bảo Hân Store")    

# Mở live tài khoản Chính LBH
@bot.message_handler(func=lambda message: message.text == "Mở live tài khoản Chính LBH")
def molive_meme(message):
    from Moudles_live.Molive_ChinhLBH import chon_nguon_chophienlive_chinhlbh, xuly_molive_chinhlbh
    chon_nguon_chophienlive_chinhlbh(message)
    bot.register_next_step_handler(message, xuly_molive_chinhlbh)

    log_info("Người dùng đã chọn mở live tài khoản Chính LBH")     

# Tắt live
@bot.message_handler(func=lambda message: message.text == "Tắt live")
def tatlive(message):
    from Moudles_live.Tatlive import xacnhan_tatlive, xuly_tatlive
    xacnhan_tatlive(message)
    bot.register_next_step_handler(message, xuly_tatlive)

    log_info("Người dùng đã chọn Tắt live từ menu chính")

# ĐỔI IP
@bot.message_handler(func=lambda message: message.text in ["Đổi IP", "Có, tiếp tục đổi IP & Thiết Bị"])
def doiip(message):
    from Moudles_live.Doi_IP import chon_taikhoan_doiip_va_thietbi, xuly_doiip_va_thietbi
    chon_taikhoan_doiip_va_thietbi(message)
    bot.register_next_step_handler(message, xuly_doiip_va_thietbi)

    log_info("Người dùng đã chọn đổi IP từ menu chính")

# Trở lại menu chính
@bot.message_handler(func=lambda message: message.text in ["Trở lại menu chính", "Trở về menu chính", "Không, trở về menu chính"])
def trolai_menuchinh(message):
    nut_menuchinh = telebot.types.ReplyKeyboardMarkup(True).add('Mở live', 'Tắt live', 'Đổi IP').add('Trở về menu chính')
    bot.send_message(message.chat.id, "VUI LÒNG CHỌN 👇", reply_markup=nut_menuchinh)

    log_info("Người dùng đã chọn trở lại menu chính")
    
# Thử nghiệm
@bot.message_handler(commands=['test'])
def test(message):
    from Moudles_live.test import chon_nguon, xuly_chonnguon

    chon_nguon(message)
    bot.register_next_step_handler(message, xuly_chonnguon)


"""" Chạy Bot """
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("LỖI")
        time.sleep(5)