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
def ask_user_timekey_ios_user(message):
    bot_reply(user_id, "Vui lòng nhập thời gian của key\nChỉ được nhập dữ liệu là số nguyên và trong khoảng từ 1-365:")
    log_info("Bot đang yêu cầu người dùng nhập thời gian của key...")

    bot.register_next_step_handler(message, main_create_key_ios_user)

def main_create_key_ios_user(message):
    global timekey
    timekey = int(message.text)
    bot_reply(user_id, f"Tiến hành tạo: 01 key\nThiết bị: IOS\nServer: IOS USER\nThời gian sử dụng key: {timekey} ngày")
    log_info(f"Người dùng đã yêu cầu tạo 1 key {timekey} ngày")
    if timekey == 1:
        create_key_1day(message)
    elif timekey == 7:
        create_key_7day(message)
    elif timekey == 30:
        create_key_30day(message)
    elif timekey == 365:
        create_key_365day(message)
    elif timekey not in [1, 7, 30, 365]:
        create_key_not_in_select(message)
    else:
        return

# HÀM TẠO KEY 1 NGÀY
def create_key_1day(message):
    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    # Tạo key bằng API của web có sẵn
    driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=128&email=nguyenhoanghuyprocoder@gmail.com&token=LOzCeWYL0Ffqj6o9w4zOWuY9NcbkyJ0zytzj8HzkQdCMTQ0ubBYz9R5K5MvxJjNDDWkNQBlo8idLJpZDjxyh7TAJ0BylLELdxRli&loaikey=1day&luotdung=1')

    try:
        bot_reply(user_id, "Đang tạo key...")
        log_info("Đang tạo key bằng API...")

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo thành công 1 key")
    except TimeoutError:
        bot_reply(user_id, "Tạo key không thành công, xảy ra sự cố kết nối internet")
        log_info("Tạo key thất bại do sự cố kết nối internet")

    try:
        # Đợi phần tử chứa key xuất hiện
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#keyDiv'))
        )
        
        # Lấy dữ liệu của phần tử chứa key
        check_key = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        key = driver.execute_script("return arguments[0].textContent;", check_key).strip()   

        # Lọc bỏ những dữ liệu không cần thiết
        clean_datakey = json.loads(key)
        key_final = clean_datakey['key']

        log_info("Gửi key đã tạo cho người dùng")
        bot_reply(user_id, "Key của bạn là:"); dylib.bot_reply(user_id, f"{key_final}")

        log_success("Gửi key cho người dùng thành công")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    except Exception as e:
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")
        bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại đường truyền của máy chủ")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return


def create_key_7day(message):
    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    # Tạo key bằng API của web có sẵn
    driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=128&email=nguyenhoanghuyprocoder@gmail.com&token=LOzCeWYL0Ffqj6o9w4zOWuY9NcbkyJ0zytzj8HzkQdCMTQ0ubBYz9R5K5MvxJjNDDWkNQBlo8idLJpZDjxyh7TAJ0BylLELdxRli&loaikey=7day&luotdung=1')

    try:
        bot_reply(user_id, "Đang tạo key...")
        log_info("Đang tạo key bằng API...")

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo thành công 1 key")
    except TimeoutError:
        bot_reply(user_id, "Tạo key không thành công, xảy ra sự cố kết nối internet")
        log_info("Tạo key thất bại do sự cố kết nối internet")

    try:
        # Đợi phần tử chứa key xuất hiện
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#keyDiv'))
        )
        
        # Lấy dữ liệu của phần tử chứa key
        check_key = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        key = driver.execute_script("return arguments[0].textContent;", check_key).strip()   

        # Lọc bỏ những dữ liệu không cần thiết
        clean_datakey = json.loads(key)
        key_final = clean_datakey['key']

        log_info("Gửi key đã tạo cho người dùng")
        bot_reply(user_id, "Key của bạn là:"); dylib.bot_reply(user_id, f"{key_final}")

        log_success("Gửi key cho người dùng thành công")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    except Exception as e:
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")
        bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại đường truyền của máy chủ")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return        

def create_key_30day(message):
    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    # Tạo key bằng API của web có sẵn
    driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=128&email=nguyenhoanghuyprocoder@gmail.com&token=LOzCeWYL0Ffqj6o9w4zOWuY9NcbkyJ0zytzj8HzkQdCMTQ0ubBYz9R5K5MvxJjNDDWkNQBlo8idLJpZDjxyh7TAJ0BylLELdxRli&loaikey=30day&luotdung=1')

    try:
        bot_reply(user_id, "Đang tạo key...")
        log_info("Đang tạo key bằng API...")

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo thành công 1 key")
    except TimeoutError:
        bot_reply(user_id, "Tạo key không thành công, xảy ra sự cố kết nối internet")
        log_info("Tạo key thất bại do sự cố kết nối internet")

    try:
        # Đợi phần tử chứa key xuất hiện
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#keyDiv'))
        )
        
        # Lấy dữ liệu của phần tử chứa key
        check_key = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        key = driver.execute_script("return arguments[0].textContent;", check_key).strip()   

        # Lọc bỏ những dữ liệu không cần thiết
        clean_datakey = json.loads(key)
        key_final = clean_datakey['key']

        log_info("Gửi key đã tạo cho người dùng")
        bot_reply(user_id, "Key của bạn là:"); dylib.bot_reply(user_id, f"{key_final}")

        log_success("Gửi key cho người dùng thành công")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    except Exception as e:
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")
        bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại đường truyền của máy chủ")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return        

def create_key_365day(message):
    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    # Tạo key bằng API của web có sẵn
    driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=128&email=nguyenhoanghuyprocoder@gmail.com&token=LOzCeWYL0Ffqj6o9w4zOWuY9NcbkyJ0zytzj8HzkQdCMTQ0ubBYz9R5K5MvxJjNDDWkNQBlo8idLJpZDjxyh7TAJ0BylLELdxRli&loaikey=365day&luotdung=1')

    try:
        bot_reply(user_id, "Đang tạo key...")
        log_info("Đang tạo key bằng API...")

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo thành công 1 key")
    except TimeoutError:
        bot_reply(user_id, "Tạo key không thành công, xảy ra sự cố kết nối internet")
        log_info("Tạo key thất bại do sự cố kết nối internet")

    try:
        # Đợi phần tử chứa key xuất hiện
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#keyDiv'))
        )
        
        # Lấy dữ liệu của phần tử chứa key
        check_key = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        key = driver.execute_script("return arguments[0].textContent;", check_key).strip()   

        # Lọc bỏ những dữ liệu không cần thiết
        clean_datakey = json.loads(key)
        key_final = clean_datakey['key']

        log_info("Gửi key đã tạo cho người dùng")
        bot_reply(user_id, "Key của bạn là:"); dylib.bot_reply(user_id, f"{key_final}")

        log_success("Gửi key cho người dùng thành công")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    except Exception as e:
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")
        bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại đường truyền của máy chủ")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return        

def create_key_not_in_select(message):
    global timekey
    timekey = message.text
    
    log_info(f"Người dùng đã yêu cầu tạo 1 key {timekey} ngày")

    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply(user_id, "Mở trang web tạo key")
    log_info("Mở trang web tạo key")
    driver.get('https://v3.ppapikey.xyz/pages/signIn')

    try:
        bot_reply(user_id, "Đang load trang web tạo key...")
        log_info("Đang load trang web tạo key")

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/nav/div')))

        bot_reply(user_id, "Load trang web tạo key thành công")
        log_success("Load trang web tạo key thành công")
    except TimeoutError:
        bot_reply(user_id, "Load trang web tạo key thất bại, vui lòng kiểm tra lại kết nối internet")
        log_error("Load trang web tạo key không thành công - xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return        

    bot_reply(user_id, "Đăng nhập vào web tạo key")
    log_info("Tiến hành dăng nhập vào web tạo key")
    
    log_info("Đang nhập tài khoản")
    driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div/div/div[2]/form/div[1]/input").send_keys('nguyenhoanghuyprocoder@gmail.com')

    log_info("Đang nhập mật khẩu")
    driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div/div/div[2]/form/div[2]/input").send_keys('123321Huy')

    log_info("Click vào nút đăng nhập")
    driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div/div/div[2]/form/div[4]/button").click()

    try:
        log_info("Đang đăng nhập...")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/nav/div/div[1]/nav/a/h6')))

        bot_reply(user_id, "Đăng nhập thành công")
        log_success("Đăng nhập thành công")
    except TimeoutError:
        bot_reply(user_id, "Đăng nhập thất bại, vui lòng kiểm tra lại kết nối internet")
        log_error("Đăng nhập thất bại - xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return        

    bot_reply(user_id, "Truy cập vào trang listkey")
    log_info("Đang truy cập vào trang listkey")
    driver.get('https://v3.ppapikey.xyz/pages/keys')

    try:
        bot_reply(user_id, "Đang load trang listkey...")
        log_info("Đang load trang listkey")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/nav/div/div[1]/nav/a/h6')))
        
        bot_reply(user_id, "Truy cập vào trang listkey thành công")
        log_success("Truy cập vào trang listkey thành công")
    except TimeoutError:
        bot_reply(user_id, "Truy cập trang listkey thất bại")
        log_error("Truy cập trang listkey thất bại")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    log_info("Click vào nút tạo key động")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div/div[4]/button[2]").click()

    #### ĐIỀN THÔNG TIN KEY ####
    bot_reply(user_id, "Tiến hành điền thông tin của key")
    log_info("Điền thông tin key")

    log_info("Đang nhập số lượng key")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div/div[2]/form/div[1]/div[1]/div/input").send_keys("1")

    log_info("Đang nhập số lượng thiết bị")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div/div[2]/form/div[1]/div[2]/div/input").send_keys("1")

    log_info("Đang nhập thời gian của key")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div/div[2]/form/div[3]/div/div/input").send_keys(timekey)

    log_info("Click vào nút tạo key")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div/div[2]/form/div[4]/div/button").click()

    try:
        bot_reply(user_id, "Điền thông tin của key hoàn tất, đang tạo key...")
        log_info("Key đang được tạo...")

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'swal2-title')))
        
        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo key thành công")
    except TimeoutError:
        bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại kết nối internet")
        log_error("Tạo key thất bại - xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return        

    bot_reply(user_id, "Key của bạn là:")
    try:
        log_info("Đợi phần tử chứa key xuất hiện")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'swal2-html-container'))
        )
        
        log_info("Đang lấy dữ liệu của key")
        key = driver.execute_script("return document.querySelector('.swal2-html-container').innerText;")
        
        bot_reply(user_id, f"{key}")
        log_info("Gửi key cho người dùng")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    except Exception as e:
        bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại kết nối internet")
        log_error("Tạo key thất bại - xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
