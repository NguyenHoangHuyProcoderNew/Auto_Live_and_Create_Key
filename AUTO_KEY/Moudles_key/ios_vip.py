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
from Moudles_support.support_chrome_driver import chromedriver_path, dir
options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)


thoigian_key = None

# Hàm yêu cầu người dùng nhập thời gian của key
def yeucau_nhap_thoigian_key_ios_vip(message):
    bot_reply(user_id, "Vui lòng nhập thời gian của key\nChỉ được nhập dữ liệu là số nguyên và trong khoảng từ 1-365:")
    log_info("Bot đang yêu cầu người dùng nhập thời gian của key...")

    bot.register_next_step_handler(message, xuly_taokey_ios_vip)

def xuly_taokey_ios_vip(message):
    global thoigian_key
    thoigian_key = timekey = int(message.text)

    bot_reply(user_id, f"Tiến hành tạo: 01 key\nThiết bị: IOS\nServer: IOS USER\nThời gian sử dụng key: {timekey} ngày")
    log_info(f"Người dùng đã yêu cầu tạo 1 key {timekey} ngày")

    if thoigian_key == 1:
        taokey_1ngay(message)
    elif thoigian_key == 7:
        taokey_7ngay(message)
    elif thoigian_key == 30:
        taokey_30ngay(message)
    elif thoigian_key == 365:
        taokey_365ngay(message)
    elif thoigian_key not in [1, 7, 30, 365]:
        taokey_thucong(message)
    else:
        return
    
def taokey_1ngay(message):
    # Nhập chức năng đóng toàn bộ trình duyệt Chrome driver cũ
    from Moudles_support.support_chrome_driver import dong_chromedriver_cu

    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome cũ")
    log_info("Đóng các phiên trình duyệt Chrome driver cũ trước khi khởi tạo Chrome driver mới")

    # Gọi hàm đóng các phiên trình duyệt Chrome driver cũ
    dong_chromedriver_cu(message)

    # Khởi tạo Chrome driver mới
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply(user_id, "Do thời gian tạo key là 1, nên tiến hành tạo key nhanh bằng API của web")
    log_info("Thời gian tạo key là 1, nên có thể tạo key nhanh bàng API từ web")

    # Tạo key bằng API của web
    try:
        driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=127&email=nguyenhoanghuyprocoder@gmail.com&token=rvyGhdjTJiXK3M1QI7gUfUxBqmrzUsRUcmP7cAZ5FQcLMlmfIbvTBJ6o9BzBcpNOYmF3gj7b96907fAQQMqVr5ciRTEfuHQBM9zy&loaikey=1day&luotdung=1')

        # Đợi tối đa 60 giây để chờ phần tử của trang web xuất hiện để đảm bảo rằng trang web đã được load hoàn tất
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, f"Tạo key bằng API thành công")
        log_info("Tạo key thành công")

        # Lấy dữ liệu của phần tử chứa mã key
        lay_dulieu_key_dau_tien = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        chuyen_makey_thanh_vanban = driver.execute_script("return arguments[0].textContent;", lay_dulieu_key_dau_tien).strip()

        # Lọc bỏ những dữ liệu không cần thiết trong mã key
        loc_dulieu_key_khongcanthiet = json.loads(chuyen_makey_thanh_vanban)
        ma_key_cuoi = loc_dulieu_key_khongcanthiet['key']

        bot_reply(user_id, f"Key của bạn là:")
        log_info("Gửi key cho người dùng")

        bot_reply(user_id, f"{ma_key_cuoi}")

    except TimeoutError:
        bot_reply(user_id, "Tạo key thất bại, xảy ra sự cố kết nối internet")
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")

def taokey_7ngay(message):
    # Nhập chức năng đóng toàn bộ trình duyệt Chrome driver cũ
    from Moudles_support.support_chrome_driver import dong_chromedriver_cu

    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome cũ")
    log_info("Đóng các phiên trình duyệt Chrome driver cũ trước khi khởi tạo Chrome driver mới")

    # Gọi hàm đóng các phiên trình duyệt Chrome driver cũ
    dong_chromedriver_cu(message)

    # Khởi tạo Chrome driver mới
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply(user_id, "Do thời gian tạo key là 1, nên tiến hành tạo key nhanh bằng API của web")
    log_info("Thời gian tạo key là 1, nên có thể tạo key nhanh bàng API từ web")

    # Tạo key bằng API của web
    try:
        driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=127&email=nguyenhoanghuyprocoder@gmail.com&token=rvyGhdjTJiXK3M1QI7gUfUxBqmrzUsRUcmP7cAZ5FQcLMlmfIbvTBJ6o9BzBcpNOYmF3gj7b96907fAQQMqVr5ciRTEfuHQBM9zy&loaikey=7day&luotdung=1')

        # Đợi tối đa 60 giây để chờ phần tử của trang web xuất hiện để đảm bảo rằng trang web đã được load hoàn tất
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, f"Tạo key bằng API thành công")
        log_info("Tạo key thành công")

        # Lấy dữ liệu của phần tử chứa mã key
        lay_dulieu_key_dau_tien = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        chuyen_makey_thanh_vanban = driver.execute_script("return arguments[0].textContent;", lay_dulieu_key_dau_tien).strip()

        # Lọc bỏ những dữ liệu không cần thiết trong mã key
        loc_dulieu_key_khongcanthiet = json.loads(chuyen_makey_thanh_vanban)
        ma_key_cuoi = loc_dulieu_key_khongcanthiet['key']

        bot_reply(user_id, f"Key của bạn là:")
        log_info("Gửi key cho người dùng")

        bot_reply(user_id, f"{ma_key_cuoi}")

    except TimeoutError:
        bot_reply(user_id, "Tạo key thất bại, xảy ra sự cố kết nối internet")
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")    

def taokey_30ngay(message):
    # Nhập chức năng đóng toàn bộ trình duyệt Chrome driver cũ
    from Moudles_support.support_chrome_driver import dong_chromedriver_cu

    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome cũ")
    log_info("Đóng các phiên trình duyệt Chrome driver cũ trước khi khởi tạo Chrome driver mới")

    # Gọi hàm đóng các phiên trình duyệt Chrome driver cũ
    dong_chromedriver_cu(message)

    # Khởi tạo Chrome driver mới
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply(user_id, "Do thời gian tạo key là 1, nên tiến hành tạo key nhanh bằng API của web")
    log_info("Thời gian tạo key là 1, nên có thể tạo key nhanh bàng API từ web")

    # Tạo key bằng API của web
    try:
        driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=127&email=nguyenhoanghuyprocoder@gmail.com&token=rvyGhdjTJiXK3M1QI7gUfUxBqmrzUsRUcmP7cAZ5FQcLMlmfIbvTBJ6o9BzBcpNOYmF3gj7b96907fAQQMqVr5ciRTEfuHQBM9zy&loaikey=30day&luotdung=1')

        # Đợi tối đa 60 giây để chờ phần tử của trang web xuất hiện để đảm bảo rằng trang web đã được load hoàn tất
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, f"Tạo key bằng API thành công")
        log_info("Tạo key thành công")

        # Lấy dữ liệu của phần tử chứa mã key
        lay_dulieu_key_dau_tien = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        chuyen_makey_thanh_vanban = driver.execute_script("return arguments[0].textContent;", lay_dulieu_key_dau_tien).strip()

        # Lọc bỏ những dữ liệu không cần thiết trong mã key
        loc_dulieu_key_khongcanthiet = json.loads(chuyen_makey_thanh_vanban)
        ma_key_cuoi = loc_dulieu_key_khongcanthiet['key']

        bot_reply(user_id, f"Key của bạn là:")
        log_info("Gửi key cho người dùng")

        bot_reply(user_id, f"{ma_key_cuoi}")

    except TimeoutError:
        bot_reply(user_id, "Tạo key thất bại, xảy ra sự cố kết nối internet")
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")    

def taokey_365ngay(message):
    # Nhập chức năng đóng toàn bộ trình duyệt Chrome driver cũ
    from Moudles_support.support_chrome_driver import dong_chromedriver_cu

    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome cũ")
    log_info("Đóng các phiên trình duyệt Chrome driver cũ trước khi khởi tạo Chrome driver mới")

    # Gọi hàm đóng các phiên trình duyệt Chrome driver cũ
    # dong_chromedriver_cu(message)

    # Khởi tạo Chrome driver mới
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply(user_id, "Do thời gian tạo key là 1, nên tiến hành tạo key nhanh bằng API của web")
    log_info("Thời gian tạo key là 1, nên có thể tạo key nhanh bàng API từ web")

    # Tạo key bằng API của web
    try:
        driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=127&email=nguyenhoanghuyprocoder@gmail.com&token=rvyGhdjTJiXK3M1QI7gUfUxBqmrzUsRUcmP7cAZ5FQcLMlmfIbvTBJ6o9BzBcpNOYmF3gj7b96907fAQQMqVr5ciRTEfuHQBM9zy&loaikey=365day&luotdung=1')

        # Đợi tối đa 60 giây để chờ phần tử của trang web xuất hiện để đảm bảo rằng trang web đã được load hoàn tất
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, f"Tạo key bằng API thành công")
        log_info("Tạo key thành công")

        # Lấy dữ liệu của phần tử chứa mã key
        lay_dulieu_key_dau_tien = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        chuyen_makey_thanh_vanban = driver.execute_script("return arguments[0].textContent;", lay_dulieu_key_dau_tien).strip()

        # Lọc bỏ những dữ liệu không cần thiết trong mã key
        loc_dulieu_key_khongcanthiet = json.loads(chuyen_makey_thanh_vanban)
        ma_key_cuoi = loc_dulieu_key_khongcanthiet['key']

        bot_reply(user_id, f"Key của bạn là:")
        log_info("Gửi key cho người dùng")

        bot_reply(user_id, f"{ma_key_cuoi}")

    except TimeoutError:
        bot_reply(user_id, "Tạo key thất bại, xảy ra sự cố kết nối internet")
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")    

def taokey_thucong(message):
    global thoigian_key
    thoigian_key = message.text

    # Nhập chức năng đóng toàn bộ trình duyệt Chrome driver cũ
    from Moudles_support.support_chrome_driver import dong_chromedriver_cu

    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome cũ")
    log_info("Đóng các phiên trình duyệt Chrome driver cũ trước khi khởi tạo Chrome driver mới")

    # Gọi hàm đóng các phiên trình duyệt Chrome driver cũ
    dong_chromedriver_cu(message)

    # Khởi tạo Chrome driver mới
    driver = webdriver.Chrome(service=service, options=options)

    # Truy cập vào trang chủ web tạo key
    bot_reply(user_id, "Tiến hành truy cập vào trang chủ web tạo key")
    log_info("Tiến hành truy cập vào trang chủ web tạo key")

    # Kiểm tra xem có truy cập trang chủ web tạo key thành công hay không
    try:
        driver.get('https://new.ppapikey.xyz/pagesMain/auth-login')

        # Đợi tối đa 60 giây để chờ phần tử của trang web xuất hiện để đảm bảo rằng trang web đã được load hoàn tất
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div')))

        bot_reply(user_id, "Truy cập vào trang chủ web tạo key thành công")
        log_success("Truy cập trang chủ web tạo key thành công")

        # Đăng nhập vào web
        bot_reply(user_id, "Tiến hành đăng nhập")
        log_info("Tiến hành đăng nhập")

        log_info("Đang nhập tài khoản")
        driver.find_element(By.ID, "username").send_keys('nguyenhoanghuyprocoder@gmail.com')
        log_info("Đang nhập mật khẩu")
        driver.find_element(By.ID, "password").send_keys('123321Huy')
        log_info("Click vào nút đăng nhập")
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[4]/button").click()

        # Kiểm tra xem có đăng nhập thành công hay không
        try:
            # Đợi tối đa 60 giây để chờ phần tử của trang web xuất hiện để đảm bảo rằng trang web đã được load hoàn tất
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/aside/ul/li[1]/a')))

            bot_reply(user_id, "Đăng nhập thành công")
            log_success("Đăng nhập thành công")

            # Truy cập vào trang listkey để tạo key
            bot_reply(user_id, "Truy cập vào trang listkey")
            log_info("Đang truy cập vào trang listkey")

            # Truy cập vào trang listkey
            driver.get('https://new.ppapikey.xyz/pagesMain/key')

            # Kiểm tra xem có truy cập trang listkey thành công hay không
            try:
                # Đợi tối đa 60 giây để chờ phần tử của trang web xuất hiện để đảm bảo rằng trang web đã được load hoàn tất
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/aside/ul/li[1]/a')))
                
                bot_reply(user_id, "Truy cập vào trang listkey thành công")
                log_success("Truy cập vào trang listkey thành công")

                # Điền thông tin key và tạo key
                log_info("Click vào nút tạo key động")
                driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/div/div/div[2]/div[4]/button[2]").click()

                bot_reply(user_id, "Tiến hành điền thông tin của key")
                log_info("Điền thông tin key")

                # log_info("Đang nhập số lượng key")
                # driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div/div[2]/form/div[1]/div[1]/div/input").send_keys("1")

                # log_info("Đang nhập số lượng thiết bị")
                # driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div/div[2]/form/div[1]/div[2]/div/input").send_keys("1")

                log_info("Đang nhập thời gian của key")
                driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/form/div[3]/div/input").clear()
                driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/form/div[3]/div/input").send_keys(thoigian_key)

                # log_info("Đang chọn server")
                # driver.find_element(By.CSS_SELECTOR, "#packageid2 > option:nth-child(2)").click()

                log_info("Click vào nút tạo key")
                driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/form/div[4]/div/button").click()

                # Kiểm tra xem có tạo key thành công hay không
                try:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'swal2-title')))
                    
                    bot_reply(user_id, "Tạo key thành công")
                    log_success("Tạo key thành công")

                    # Lấy dữ liệu của mã key và gửi cho người dùng
                    try:
                        # Đợi phần tử chứa mã key xuất hiện
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, 'swal2-html-container'))
                        )
                        
                        # Lấy dữ liệu của phần tử chứa mã key
                        key = driver.execute_script("return document.querySelector('.swal2-html-container').innerText;")

                        # Gửi key cho người dùng
                        bot_reply(user_id, "Key của bạn là:")
                        log_info("Đang lấy dữ liệu của key")
                        
                        bot_reply(user_id, f"{key}")
                        log_info("Gửi key cho người dùng")

                        log_info("Đóng trình duyệt chrome")
                        driver.quit()

                        log_info("Kết thúc tiến trình")
                        return
                    except Exception as e:
                        bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại kết nối internet")
                        log_error("Tạo key thất bại - xảy ra sự cố kết nối internet")

                        log_info("Đóng trình duyệt Chrome")
                        driver.quit()

                        log_info("Kết thúc tiến trình")
                        return
                except TimeoutError:
                    bot_reply(user_id, "Tạo key thất bại, vui lòng kiểm tra lại kết nối internet")
                    log_error("Tạo key thất bại - xảy ra sự cố kết nối internet")

                    log_info("Đóng trình duyệt chrome")
                    driver.quit()

                    log_info("Kết thúc tiến trình")
                    return  
            except TimeoutError:
                bot_reply(user_id, "Truy cập trang listkey thất bại, xảy ra sự cố kết nối interntet")
                log_error("Truy cập trang listkey thất bại, xảy ra sự cố kết nối internet")

                log_info("Đóng trình duyệt Chrome")
                driver.quit()

                log_info("Kết thúc tiến trình")
                return
        except TimeoutError:
            bot_reply(user_id, "Đăng nhập thất bại, vui lòng kiểm tra lại kết nối internet")
            log_error("Đăng nhập thất bại - xảy ra sự cố kết nối internet")

            log_info("Đóng trình duyệt chrome")
            driver.quit()

            log_info("Kết thúc tiến trình")
            return 
    except TimeoutError:
        bot_reply(user_id, "Load trang web tạo key thất bại, vui lòng kiểm tra lại kết nối internet")
        log_error("Load trang web tạo key không thành công - xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return  