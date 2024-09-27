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

# Trở lại menu chính
def trolai_menuchinh(message):
    nut_menuchinh = telebot.types.ReplyKeyboardMarkup(True).add('Mở live', 'Tắt live', 'Đổi IP').add('Trở về menu chính')
    bot.send_message(message.chat.id, "VUI LÒNG CHỌN 👇", reply_markup=nut_menuchinh)

# Yêu cầu người dùng chọn tài khoản cần đổi IP & Thiết Bị
def chon_taikhoan_doiip_va_thietbi(message):
    # Tạo nút chọn tài khoản cần đổi IP & Thiết Bị
    button_chontaikhoan = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP Tài khoản Tấn Tài", "Đổi IP Tài khoản Phụ LBH", "Đổi IP Tài khoản Meme").add("Đổi IP Tài khoản Bảo Hân Store", "Đổi IP Tài khoản Chính LBH").add("Trở lại menu chính")

    # Hỏi người dùng muốn chọn tài khoản nào để đổi IP & Thiết Bị
    bot.send_message(message.chat.id, "Bạn muốn đổi IP tài khoản nào?", reply_markup=button_chontaikhoan)

    bot.register_next_step_handler(message, xuly_doiip_va_thietbi)   

# Xử lý quá trình đổi IP & Thiết Bị
def xuly_doiip_va_thietbi(message):
    # Nhập hàm đóng trình duyệt Chrome driver cũ
    from Moudles_support.support_chrome_driver import dong_chromedriver_cu

    # Kiểm tra sự lựa chọn của người dùng
    if message.text == "Đổi IP Tài khoản Tấn Tài":
        from Moudles_support.support_bot import doiip_tantai, doi_thietbi_tantai
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị cho Tài khoản Tấn Tài")
        log_info(f"Người dùng đã chọn Đổi IP Tài khoản Tấn Tài")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        ip = doiip_tantai
        thietbi = doi_thietbi_tantai
    elif message.text == "Đổi IP Tài khoản Phụ LBH":
        from Moudles_support.support_bot import doiip_nickphulbh, doi_thietbi_nickphulbh
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị Tài khoản Phụ LBH")
        log_info(f"Người dùng đã chọn Đổi IP Tài khoản Phụ LBH")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        ip = doiip_nickphulbh
        thietbi = doi_thietbi_nickphulbh
    elif message.text == "Đổi IP Tài khoản Meme":
        from Moudles_support.support_bot import doiip_meme, doi_thietbi_meme
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị Tài khoản Meme")
        log_info(f"Người dùng đã chọn Đổi IP Tài khoản Meme")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        ip = doiip_meme
        thietbi = doi_thietbi_meme
    elif message.text == "Đổi IP Tài khoản Bảo Hân Store":
        from Moudles_support.support_bot import doiip_baohanstore, doi_thietbi_baohanstore
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị Tài khoản Bảo Hân Store")
        log_info(f"Người dùng đã chọn Đổi IP Tài khoản Bảo Hân Store")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        ip = doiip_baohanstore
        thietbi = doi_thietbi_baohanstore
    elif message.text == "Đổi IP Tài khoản Chính LBH":
        from Moudles_support.support_bot import doiip_chinhlbh, doi_thietbi_chinhlbh
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị Tài khoản Chính LBH")
        log_info(f"Người dùng đã chọn Đổi IP Tài khoản Chính LBH")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        ip = doiip_chinhlbh
        thietbi = doi_thietbi_chinhlbh        
    
    elif message.text == "Trở lại menu chính":
        trolai_menuchinh(message)
        return
    else:
        bot_reply(user_id, "Lựa chọn không hợp lệ, hiện không có tài khoản này")
        trolai_menuchinh(message)
        return

    # Đóng các phiên trình duyệt Chrome driver cũ
    log_info("Đóng các phiên Chrome driver cũ")
    # Hàm đóng các phiên trình duyệt Chrome driver cũ
    dong_chromedriver_cu(message)

    # Khởi tạo Chrome driver mới
    driver = webdriver.Chrome(service=service, options=options)
    
    # Kiểm tra xem có truy cập web livestream thành công hay không
    try:
        # Mở trang web livestream
        log_info("Truy cập vào trang web livestream")
        driver.get('https://autolive.one/tiktok')

        # Chờ element được chỉ định xuất hiện để xác định có truy cập trang thành công hay không
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        bot_reply(user_id, "Truy cập trang web livestream thành công")
        log_success("Truy cập vào trang web livestream thành công")

        # Click vào nút đổi TK Web
        log_info("Click vào nút đổi TK Web")
        driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(3) > div.col-md-3 > div > div > button:nth-child(2) > i").click()

        # Chờ element được chỉ định xuất hiện để chờ giao diện web thay đổi sau khi click vào nút đổi TK Web
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dialog_tiktok > div > div > div")))

        # Xử lý quá trình đổi IP
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

           # Xử lý đổi Thiết Bị
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
                    log_info("Click vào nút đổi Thiết Bị")
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
                        tieptuc_doiip_va_thietbi_hoac_dunglai(message)

                        # Kết thúc tiến trình
                        return
                    else:
                        log_error(f"Đổi Thiết Bị thất bại - Thông báo từ web: {thongbao_doithietbi}")
                        bot_reply(user_id, f"Đổi Thiết Bị thất bại - Thông báo từ web: {thongbao_doithietbi}")

                        log_info("Đóng trình duyệt chrome")
                        driver.quit()

                        """"Hỏi người dùng có muốn tiếp tục không?"""
                        tieptuc_doiip_va_thietbi_hoac_dunglai(message)

                        # Kết thúc tiến trình
                        return
                except TimeoutError:
                    bot_reply(user_id, "Đổi Thiết Bị thất bại, thông báo không xuất hiện trong thời gian chờ quy định")
                    log_error("Đổi Thiết Bị thất bại, thông báo không xuất hiện trong thời gian chờ quy định")

                    log_info("Đóng trình duyệt Chrome")
                    driver.quit()

                    log_info("Kết thúc tiến trình")
                    return
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

            log_info("Đóng trình duyệt Chrome")
            driver.quit()

            log_info("Kết thúc tiến trình")
            return
    except TimeoutError:
        bot_reply(user_id, "Truy cập trang web livestream không thành công, xảy ra sự cố kết nối internet")
        log_error("Không thể truy cập trang web livestream, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
        
# Hỏi người dùng có muốn tiếp tục không? Hay dừng lại và trở về menu chính
def tieptuc_doiip_va_thietbi_hoac_dunglai(message):
    nut_tieptuc_doiip_va_thietbi_hoac_dunglai = telebot.types.ReplyKeyboardMarkup(True).add("Có, tiếp tục đổi IP & Thiết Bị").add("Không, trở về menu chính")
    bot.send_message(message.chat.id, "Bạn có muốn tiếp tục nữa không?", reply_markup=nut_tieptuc_doiip_va_thietbi_hoac_dunglai)    
    log_info("Đang hỏi người dùng có muốn tiếp tục đổi IP không hay về menu chính")