# Import các thư viện cần thiết
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
import pyperclip
from selenium.common.exceptions import NoSuchElementException
logging.basicConfig(level=logging.CRITICAL)  # Chỉ in thông báo lỗi nghiêm trọng
import datetime
now = datetime.datetime.now()
from selenium.common.exceptions import TimeoutException
from colorama import Fore, Style, init

# NHẬP FILE DYLIB CHỨA CÁC HÀM QUAN TRỌNG
from dylib import dylib

import json

# CẤU HÌNH WEBDRIVER
chromedriver_path = r'D:\\BOT_TELE_AUTO_WORK\\BOT AUTO KEY\\chrome_driver\\chromedriver1.exe'

options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

# CÁC CHỨC NĂNG IN RA MÀN HÌNH
from print_logger.print_logger import log_info, log_warning, log_error, log_success

# Nhập chức năng bot phản hồi lại người dùng
from dylib.dylib import bot_reply

from dylib.dylib import user_id
from dylib.dylib import username

timekey = None

# HÀM YÊU CẦU NGƯỜI DÙNG NHẬP THỜI GIAN SỬ DỤNG CỦA KEY
def ask_user_timekey_android(message):
    bot_reply(user_id, "Vui lòng nhập thời gian của key\nChỉ được nhập dữ liệu là số nguyên và trong khoảng từ 1-30:")
    log_info("Bot đang yêu cầu người dùng nhập thời gian của key...")

    bot.register_next_step_handler(message, main_create_key_android)

# HÀM CHÍNH XỬ LÝ CÁC TÁC VỤ ĐỂ TẠO KEY
def main_create_key_android(message):
    from dylib.dylib import close_existing_browser
    global timekey
    timekey = int(message.text)

    bot_reply(user_id, f"Tiến hành tạo: 01 key\nTHÔNG TIN KEY\nThiết bị hỗ trợ: ANDROID\nSố lượng thiết bị sử dụng: 01 thiết bị\nThời gian sử dụng key: {timekey} ngày")
    log_info(f"Người dùng đã yêu cầu tạo 1 key {timekey} ngày")


    log_info("Đang chạy hàm kiểm tra các phiên trình duyệt đang chạy, nếu có phiên trình duyệt nào đang được sẽ đóng trình duyệt")
    close_existing_browser() # Đóng tất cả các phiên trình duyệt đang chạy
    
    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply(user_id, "Đang mở trang tạo key")
    log_info("Đang mở trang tạo key")
    driver.get('https://mypanelhuymapsang.000webhostapp.com/login')

    try:
        bot_reply(user_id, "Đang tải trang web tạo key...")
        log_info("Đang tải trang web tạo key")

        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div/a')))
        
        bot_reply(user_id, "Load trang web tạo key thành công")
        log_success("Tải trang web tạo key thành công")
    except TimeoutException:
        bot_reply(user_id, "Load trang web tạo key thất bại, vui lòng kiểm tra lại kết nối internet")
        log_error("Load trang web tạo key không thành công - xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return  

    bot_reply(user_id, "Đăng nhập vào web tạo key")
    log_info("Tiến hành dăng nhập vào web tạo key")

    log_info("Đang nhập tài khoản")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[1]/input").send_keys('HUYMAPSANG')

    log_info("Đang nhập mật khẩu")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[2]/input").send_keys('99999999')
    
    log_info("Click vào nút đăng nhập")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[5]/button").click()

    try:
        log_info("Đang đăng nhập...")
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[2]/div/div[1]')))

        bot_reply(user_id, "Đăng nhập thành công")
        log_success("Đăng nhập thành công")
    except TimeoutException:
        bot_reply(user_id, "Đăng nhập thất bại, vui lòng kiểm tra lại kết nối internet")
        log_error("Đăng nhập thất bại - xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return  

    bot_reply(user_id, "Truy cập vào trang listkey")
    log_info("Đang truy cập vào trang listkey")
    driver.get('https://mypanelhuymapsang.000webhostapp.com/keys/generate')

    try:
        bot_reply(user_id, "Đang load trang listkey...")
        log_info("Đang load trang listkey")

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[2]/div[1]/div/div[1]')))

        bot_reply(user_id, "Truy cập vào trang listkey thành công")
        log_success("Truy cập vào trang listkey thành công")
    except TimeoutException:
        bot_reply(user_id, "Truy cập trang listkey thất bại")
        log_error("Truy cập trang listkey thất bại")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    bot_reply(user_id, "Tiến hành điền thông tin của key")
    log_info("Điền thông tin key")

    # CHỌN THỜI GIAN KEY
    log_info("Đang chọn thời gian của key")
    select_day_option = f'#duration > option:nth-child({timekey + 2})'
    # Click chọn thời gian key
    driver.find_element(By.CSS_SELECTOR, select_day_option).click()

    try:
        bot_reply(user_id, "Điền thông tin của key hoàn tất, đang tạo key...")
        log_info("Click vào nút tạo key") 

        # Click vào nút TẠO KEY
        driver.find_element(By.CSS_SELECTOR, "body > main > div > div > div > div.card > div.card-body > form > div:nth-child(5) > button").click()

        log_info("Key đang được tạo...")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[1]')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo key thành công")
    except TimeoutException:
        bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại kết nối internet")
        log_error("Tạo key thất bại - xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return 

    bot_reply(user_id, "Key của bạn là:")

    try:
        log_info("Đợi phần tử chứa key xuất hiện")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert.alert-success')))

        key = driver.execute_script("return document.querySelector('.alert.alert-success strong').innerText;")

        bot_reply(user_id, f"{key}")
        log_info("Gửi key cho người dùng")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    except Exception:
        bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại kết nối internet")
        log_error("Tạo key thất bại - xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return