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
import json
# Nhập chức năng in log ra màn hình
from Moudles_support.print_log import log_error, log_info, log_success

# Nhập chức năng bot phản hồi lại người dùng
from Moudles_support.support_bot import bot_reply, API_TOKEN

# ID của ADMIN Bot
from Moudles_support.support_bot import user_id

# Cấu hình API telegram
# API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w' # Token của BOT
bot = telebot.TeleBot(API_TOKEN)

# Cấu hình Chrome driver
from Moudles_support.support_chrome_driver import chromedriver_path
options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

thoigian_key = None

def yeucau_nhap_thoigian_key_android(message):
    bot_reply(user_id, "Vui lòng nhập thời gian của key\nChỉ được nhập dữ liệu là số nguyên và trong khoảng từ 1-30:")
    log_info("Bot đang yêu cầu người dùng nhập thời gian của key...")

    bot.register_next_step_handler(message, xuly_taokey_android)

def xuly_taokey_android(message):
    # Nhập chức năng đóng toàn bộ trình duyệt Chrome driver cũ
    from Moudles_support.support_chrome_driver import dong_chromedriver_cu

    global thoigian_key
    thoigian_key = int(message.text)

    bot_reply(user_id, f"Tiến hành tạo: 01 key\nTHÔNG TIN KEY\nThiết bị hỗ trợ: ANDROID\nSố lượng thiết bị sử dụng: 01 thiết bị\nThời gian sử dụng key: {thoigian_key} ngày")
    log_info(f"Người dùng đã yêu cầu tạo 1 key {thoigian_key} ngày")

    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome cũ")
    log_info("Đóng các phiên trình duyệt Chrome driver cũ trước khi khởi tạo Chrome driver mới")

    # Gọi hàm đóng các phiên trình duyệt Chrome driver cũ
    dong_chromedriver_cu(message)

    # Khởi tạo Chrome driver mới
    driver = webdriver.Chrome(service=service, options=options)

    # Truy cập vào trang tạo key
    bot_reply(user_id, "Truy cập vào trang chủ web tạo key")
    log_info("Truy cập vào trang chủ web tạo key")

    driver.get('https://mypanelhuymapsang.000webhostapp.com/login')

    # Kiểm tra xem có truy cập vào trang chủ web tạo key thành công hay không
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div/a')))
        
        bot_reply(user_id, "Truy cập trang chủ web tạo key thành công")
        log_success("Truy cập trang chủ web tạo key thành công")

        # Đăng nhập vào web tạo key
        bot_reply(user_id, "Đăng nhập vào web tạo key")
        log_info("Tiến hành dăng nhập vào web tạo key")

        log_info("Đang nhập tài khoản")
        driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[1]/input").send_keys('HUYMAPSANG')

        log_info("Đang nhập mật khẩu")
        driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[2]/input").send_keys('99999999')
        
        log_info("Click vào nút đăng nhập")
        driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[5]/button").click()

        # Kiểm tra xem có đăng nhập vào web tạo key thành công hay không
        try:
            WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[2]/div/div[1]')))

            bot_reply(user_id, "Đăng nhập thành công")
            log_success("Đăng nhập thành công")

            # Truy cập vào trang listkey
            bot_reply(user_id, "Truy cập vào trang listkey")
            log_info("Đang truy cập vào trang listkey")

            driver.get('https://mypanelhuymapsang.000webhostapp.com/keys/generate')

            # Kiểm tra xem có truy cập trang listkey thành công hay không
            try:
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[2]/div[1]/div/div[1]')))

                bot_reply(user_id, "Truy cập vào trang listkey thành công")
                log_success("Truy cập vào trang listkey thành công")

                # Điền thông tin của key
                bot_reply(user_id, "Tiến hành điền thông tin của key")
                log_info("Điền thông tin key")

                log_info("Đang chọn thời gian của key")
                chonthoigian_key = f'#duration > option:nth-child({thoigian_key + 2})'
                driver.find_element(By.CSS_SELECTOR, chonthoigian_key).click()

                log_info("Click vào nút TẠO KEY")
                driver.find_element(By.CSS_SELECTOR, "body > main > div > div > div > div.card > div.card-body > form > div:nth-child(5) > button").click()

                # Kiểm tra xem có tạo key thành công hay không
                try:
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[1]')))

                    bot_reply(user_id, "Tạo key thành công")
                    log_success("Tạo key thành công")

                    # Lấy dữ liệu của phần tử chứa mã key
                    key = driver.execute_script("return document.querySelector('.alert.alert-success strong').innerText;")

                    # Gửi key cho người dùng
                    bot_reply(user_id, "Key của bạn là:")
                    bot_reply(user_id, f"{key}")
                    log_info("Gửi key cho người dùng")

                    log_info("Đóng trình duyệt Chrome")
                    driver.quit()

                    log_info("Kết thúc tiến trình")
                    return

                except TimeoutError:
                    bot_reply(user_id, "Tạo key thất bại, xảy ra sự cố kết nối internet")
                    log_error("Tạo key thất bại - xảy ra sự cố kết nối internet")

                    log_info("Đóng trình duyệt Chrome")
                    driver.quit()

                    log_info("Kết thúc tiến trình")
                    return 
            except TimeoutError:
                bot_reply(user_id, "Truy cập trang listkey thất bại, xảy ra sự cố kết nối internet")
                log_error("Truy cập trang listkey thất bại - xảy ra sự cố kết nối internet")

                log_info("Đóng trình duyệt Chrome")
                driver.quit()

                log_info("Kết thúc tiến trình")
                return
        except TimeoutError:
            bot_reply(user_id, "Đăng nhập thất bại, xảy ra sự cố kết nối internet")
            log_error("Đăng nhập thất bại - xảy ra sự cố kết nối internet")

            log_info("Đóng trình duyệt Chrome")
            driver.quit()

            log_info("Kết thúc tiến trình")
            return  
    except TimeoutError:
        bot_reply(user_id, "Truy cập trang chủ web tạo key thất bại, xảy ra sự cố kết nối internet")
        log_error("Truy cập trang chủ web tạo key thát bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return  