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
from selenium.common.exceptions import TimeoutException
from colorama import Fore, Style, init
from telebot import types

# Cấu hình API telegram
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc' # Token của BOT
bot = telebot.TeleBot(API_TOKEN)

# Cấu hình Chrome driver
from Moudles_support.support_chrome_driver import chromedriver_path, dir
options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument(f'--user-data-dir={dir}')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# Nhập chức năng in log ra màn hình
from Moudles_support.print_log import log_error, log_info, log_success

# Nhập chức năng bot phản hồi lại người dùng
from Moudles_support.support_bot import bot_reply

# ID của ADMIN Bot
from Moudles_support.support_bot import user_id

# Khai báo biến toàn cục cho IP & Thiết bị
ip = None
thietbi = None

# Trở lại menu chính
def trolai_menuchinh(message):
    nut_menuchinh = telebot.types.ReplyKeyboardMarkup(True).add('Mở live', 'Tắt live', 'Đổi IP').add('Trở về menu chính')
    bot.send_message(message.chat.id, "VUI LÒNG CHỌN 👇", reply_markup=nut_menuchinh)

# Yêu cầu người dùng chọn tài khoản cần đổi IP & Thiết Bị
def chon_taikhoan_doiip_va_thietbi(message):
    # Tạo nút chọn tài khoản cần đổi IP & Thiết Bị
    button_chontaikhoan = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP Tài khoản Văn Bảo").add("Đổi IP Tài khoản Phụ LBH").add("Đổi IP Tài khoản Meme").add("Trở lại menu chính")
    bot.send_message(message.chat.id, "Bạn muốn đổi IP tài khoản nào?", reply_markup=button_chontaikhoan)

    bot.register_next_step_handler(message, xuly_doiip)   

"""" Xử lý đổi IP """
def xuly_doiip(message):
    """"Nhập chức năng đóng toàn bộ trình duyệt Chrome trước khi khởi tạo Chrome driver mới"""
    from Moudles_support.support_chrome_driver import dong_toanbo_trinhduyet_chrome

    global ip
    global thietbi

    if message.text == "Đổi IP Tài khoản Văn Bảo":
        ip = "ip-23816"
        thietbi = "renew-23816"
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị cho Tài khoản Văn Bảo")
        log_info(f"Người dùng đã chọn Đổi IP Tài khoản Văn Bảo")
    elif message.text == "Đổi IP Tài khoản Phụ LBH":
        ip = "ip-22679"
        thietbi = "renew-22679"
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị Tài khoản Phụ LBH")
        log_info(f"Người dùng đã chọn Đổi IP Tài khoản Phụ LBH")
    elif message.text == "Đổi IP Tài khoản Meme":
        ip = "ip-22733"
        thietbi = "renew-22733"
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị Tài khoản Nick Meme Lỏ")
        log_info(f"Người dùng đã chọn Đổi IP Tài khoản Meme")
    elif message.text == "Trở lại menu chính":
        trolai_menuchinh(message)
        return
    else:
        bot_reply(user_id, "Lựa chọn không hợp lệ, trở về menu chính")
        trolai_menuchinh(message)
        return

    # Đóng các phiên trình duyệt Chrome driver cũ
    bot_reply(user_id, "Đang đóng các phiên trình duyệt Chrome driver cũ")
    log_info("Đóng các phiên Chrome driver cũ")

    # Hàm đóng các phiên trình duyệt Chrome driver cũ
    dong_toanbo_trinhduyet_chrome(message) 

    # Khởi tạo Chrome driver mới
    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome driver cũ hoàn tất")
    bot_reply(user_id,"Khởi tạo Chrome driver mới")
    log_info("Khởi tạo chrome driver")

    # Biến khởi tạo Chrome driver mới
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply(user_id, "Truy cập vào trang web livestream")
    log_info("Truy cập vào trang web livestream")
    
    # Kiểm tra xem có truy cập web livestream thành công hay không
    try:
        # Mở trang web livestream
        driver.get('https://autolive.one/tiktok')

        # Đợi phần tử trên trang web xuất hiện để xác định có truy cập trang web thành công hay không
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        bot_reply(user_id, "Truy cập trang web livestream thành công")
        log_success("Truy cập vào trang web thành công")

        # Click vào nút đổi TK Web
        log_info("Click vào nút đổi TK Web")
        driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(3) > div.col-md-3 > div > div > button:nth-child(2) > i").click()

        # Đợi giao diện của web sau khi click vào nút đổi TK Web xuất hiện
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dialog_tiktok > div > div > div")))

        """"Xử lý đổi IP"""
        try:
            bot_reply(user_id, "Tiến hành đổi IP...")

            # Click vào nút Đổi IP
            log_info("Click vào nút đổi IP")
            driver.execute_script("document.getElementById(arguments[0]).click();", ip)

            # Chờ thông báo của web xuất hiện sau khi click vào nút Đổi IP
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))
            
            # Lấy dữ liệu của thông báo từ web sau khi click vào nút đổi IP
            thongbao_doiip = driver.execute_script('''
                // JavaScript code here
                // Đoạn mã JavaScript để lấy nội dung của phần tử
                var element = document.querySelector('div.text[data-notify-html="text"]');
                return element.textContent;
            ''')

            # Kiểm tra xem có đổi IP thành công hay không
            if thongbao_doiip == "Thành công":
                bot_reply(user_id, "Đổi IP thành công")
                log_success("Đổi IP thành công")
            else:
                log_error(f"Đổi IP thất bại - Nguyên nhân: {thongbao_doiip}")
                bot_reply(user_id, f"Đổi IP thất bại - {thongbao_doiip}")

            """"Xử lý đổi Thiết Bị"""
            bot_reply(user_id, "Làm mới lại trang web livestream trước khi tiến hành đổi thiết bị")
            log_info("Làm mới lại trang web trước khi tiến hành đổi thiết bị")

            driver.refresh() # Làm mới lại trang web livestream

            # Kiểm tra xem có làm mới lại trang web livestream trước khi đổi thiết bị thành công hay không
            try:
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

                bot_reply(user_id, "Làm mới trang web livestream thành công")
                log_success("Làm mới lại trang web livestream trước khi tiến hành đổi thiết bị thành công")

                # Tiến hành đổi thiết bị sau khi làm mới trang web thành công
                bot_reply(user_id, "Tiến hành đổi Thiết Bị...")

                # Click vào nút đổi TK Web
                log_info("Click vào nút đổi TK Web")
                driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(3) > div.col-md-3 > div > div > button:nth-child(2) > i").click()

                # Đợi giao diện của web sau khi click vào nút đổi TK Web xuất hiện
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dialog_tiktok > div > div > div")))

                # Kiểm tra xem có đổi Thiết Bị thành công hay không
                try:
                    # Click vào nút Đổi Thiết Bị
                    driver.execute_script("document.getElementById(arguments[0]).click();", thietbi)

                    # Chờ thông báo của web xuất hiện sau khi click vào nút Đổi Thiết Bị
                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

                    # Lấy dữ liệu của thông báo web livestream sau khi click vào nút đổi Thiết Bị
                    thongbao_doithietbi = driver.execute_script('''
                        // JavaScript code here
                        // Đoạn mã JavaScript để lấy nội dung của phần tử
                        var element = document.querySelector('div.text[data-notify-html="text"]');
                        return element.textContent;
                    ''')

                    # Kiểm tra dữ liệu của thông báo
                    if thongbao_doithietbi == "Thành công":
                        bot_reply(user_id, "Đổi Thiết Bị thành công")
                        log_success(f"Đổi Thiết Bị thành công - Thông báo từ web: {thongbao_doithietbi}") 

                        log_info("Đóng trình duyệt chrome")
                        driver.quit()

                        # Gọi hàm hỏi người dùng có muốn tiếp tục đổi IP hay không
                        tieptucdoiip_hoac_dungdoiip(message)

                        # Kết thúc tiến trình
                        return
                    else:
                        log_error(f"Đổi Thiết Bị thất bại - Thông báo từ web: {thongbao_doithietbi}")
                        bot_reply(user_id, f"Đổi Thiết Bị thất bại - Thông báo từ web: {thongbao_doithietbi}")

                        log_info("Đóng trình duyệt chrome")
                        driver.quit()

                        """"Hỏi người dùng có muốn tiếp tục không?"""
                        tieptucdoiip_hoac_dungdoiip(message)

                        # Kết thúc tiến trình
                        return
                except TimeoutError:


            except TimeoutError:
                bot_reply(user_id, "Làm mới trang web livestream thất bại, xảy ra sự cố kết nối internet")
                log_error("Truy cập vào trang web thất bại, xảy ra sự cố kết nối internet")

                log_info("Đóng trình duyệt Chrome")
                driver.quit()

                log_info("Kết thúc tiến trình")
                return
            

        except TimeoutError:
            bot_reply(user_id, "Đổi IP thất bại, do không thể lấy được dữ liệu của thông báo trong thời gian chờ quy định")
            log_error("Đổi IP thất bại do thông báo sau khi đổi IP không xuất hiện trong thời gian chờ quy định")
    except TimeoutError:
        bot_reply(user_id, "Truy cập trang web livestream không thành công, xảy ra sự cố kết nối internet")
        log_error("Không thể truy cập trang web livestream, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    

    """ Làm mới lại trang web livestream sau khi đổi IP"""


    """" Click vào nút đổi Thêm Tk bằng web để đổi thiết bị"""
    log_info("Click vào nút Đổi TK Web")
    driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(3) > div.col-md-3 > div > div > button:nth-child(2) > i").click()

    # Đợi giao diện sau khi click vào nút thêm Tk bằng Web xuất hiện
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dialog_tiktok > div > div > div")))

    
""" Hỏi người dùng xem có muốn tiếp tục đổi IP không?"""
def tieptucdoiip_hoac_dungdoiip(message):
    nut_tieptucdoiip_hoac_dungdoiip = telebot.types.ReplyKeyboardMarkup(True).add("Có, tiếp tục đổi IP").add("Không, trở về menu chính")
    bot.send_message(message.chat.id, "Bạn có muốn tiếp tục nữa không?", reply_markup=nut_tieptucdoiip_hoac_dungdoiip)    
    log_info("Đang hỏi người dùng có muốn tiếp tục đổi IP không hay về menu chính")