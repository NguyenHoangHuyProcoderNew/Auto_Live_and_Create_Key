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

"""" Trở lại menu chính """
def trolai_menuchinh(message):
    nut_menuchinh = telebot.types.ReplyKeyboardMarkup(True).add('Mở live', 'Tắt live', 'Đổi IP').add('Trở về menu chính')
    bot.send_message(message.chat.id, "VUI LÒNG CHỌN 👇", reply_markup=nut_menuchinh)

"""" Yêu cầu người dùng xác nhận tắt phiên live """
def xacnhan_tatlive(message):
    # Tạo nút xác nhận tắt live
    xacnhantatlive = telebot.types.ReplyKeyboardMarkup(True)
    xacnhantatlive.add('Có', 'Không').add('Trở lại menu chính')
    bot.send_message(message.chat.id, "Xác nhận tắt phiên live hiện tại?", reply_markup=xacnhantatlive)
    log_info(f"Bot đang yêu cầu người dùng xác nhận tắt phiên live")

    # Sau khi người dùng xác nhận gọi hàm main_tatlive để xử lý
    bot.register_next_step_handler(message, xuly_tatlive)

"""" Xử lý tắt live """
def xuly_tatlive(message):
    # Kiểm tra sự lựa chọn của người dùng
    if message.text == "Có":
        # Nhập chức năng đóng trình duyệt Chrome driver cũ
        from Moudles_support.support_chrome_driver import dong_chromedriver_cu

        # Gọi chức năng đóng trình duyệt Chrome driver cũ
        bot_reply(user_id, "Đóng các phiên trình duyệt Chrome driver cũ")
        log_info("Chạy hàm đóng các phiên trình duyệt Chrome driver cũ")

        dong_chromedriver_cu(message) # Chạy hàm đóng các phiên trình duyệt Chrome driver cũ

        # Khởi tạo Chrome driver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Kiểm tra xem có truy cập web livestream thành công hay không
        try:
            bot_reply(user_id, "Mở trang web live")
            log_info("Truy cập vào trang web live")

            driver.get('https://autolive.me/tiktok')

            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

            bot_reply(user_id, "Mở trang web live thành công")
            log_success("Truy cập vào trang web live thành công")
        except TimeoutError:
            bot_reply(user_id, "Mở trang web thất bại, xảy ra sự cố kết nối internet")
            log_error("Truy cập vào trang web thất bại, xảy ra sự cố kết nối internet")

            log_info("Đóng trình duyệt Chrome")
            driver.quit()

            log_info("Kết thúc tiến trình")
            return

        # Xử lý quá trình tắt live
        while True:
            try:
                bot_reply(user_id, "Đang đợi nút Dừng live xuất hiện")
                log_info("Đợi nút Dừng live xuất hiện")

                #  Chờ nút tắt phiên live xuất hiện
                nut_dunglive = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-original-title='Dừng live']"))
                )
                bot_reply(user_id, "Nút Dừng live đã xuất hiện")

                # Kiểm tra Tiêu đề của nút, nếu là "Dừng live" thì mới thực hiện click vào nút để tắt phiên live
                if nut_dunglive.get_attribute("data-original-title") == "Dừng live":
                    nut_dunglive.click() # Click vào nút tắt live

                    bot_reply(user_id, "Click vào nút Dừng live thành công, đang đợi thông báo từ web...")
                    log_info("Click vào nút Dừng live - đợi thông báo từ web sau khi click")

                    # Đợi thông báo từ web xuất hiện sau khi click vào nút tắt live
                    try:
                        # Chờ thông báo xuất hiện
                        WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div > div.notifyjs-container > div'))
                        )
                        
                        # Lấy nội dung của thông báo
                        thongbao_tatlive = driver.execute_script('''
                        // JavaScript code here
                        // Đoạn mã JavaScript để lấy nội dung của phần tử
                        var element = document.querySelector('div.text[data-notify-html="text"]');
                        return element.textContent;
                    ''')
                        
                        # Kiểm tra nội dung của thông báo
                        if thongbao_tatlive == "Success":
                            bot_reply(user_id, f"Tắt live thành công - Thông báo từ web: {thongbao_tatlive}")
                            log_success(f"Tắt lice thành công, thông báo từ web: {thongbao_tatlive}")

                            # Kiểm tra phần tử Trạng thái để xác định thời điểm có thể khởi tạo phiên live mới
                            bot_reply(user_id, "Tiến hành kiểm tra Trạng thái luồng live")
                            log_info("Kiểm tra Trạng thái luồng live")

                            while True:
                                # Lấy dữ liệu của phần tử Trạng thái
                                dulieu_trangthai = driver.find_element(By.CSS_SELECTOR, "td.text-center:nth-child(10)").text

                                # Kiểm tra phần tử Trạng thái
                                if dulieu_trangthai == "Mới":
                                    bot_reply(user_id, "Phiên live đã được tắt hoàn toàn, bạn có thể khởi tạo phiên live mới ngay bây giờ")
                                    log_success("Phiên live đã được tắt hoàn toàn")
                                
                                    log_info("Đóng trình duyệt Chrome")
                                    driver.quit()

                                    log_info("Kết thúc tiến trình")
                                    return
                                else:
                                    bot_reply(user_id, f"Trạng thái của luồng live sau khi click vào nút tắt live là: {dulieu_trangthai}")
                                    bot_reply(user_id, f"Làm mới lại trang web")

                                    log_error("Dữ liệu của phần tử Trạng thái chưa hợp lệ, làm mới lại trang web")

                                    # Cho làm mới lại trang web
                                    driver.refresh()

                                    # Kiểm tra xem có làm mới lại trang web livestream thành công hay không
                                    try:
                                        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

                                        bot_reply(user_id, "Làm mới trang web livestream thành công")
                                        log_success("Làm mới trang web thành công")
                                    except TimeoutError:
                                        bot_reply(user_id, "Làm mới trang web thất bại, xảy ra sự cố kết nối internet")
                                        log_error("Làm mới trang web thất bại, xảy ra sự cố kết nối internet")

                                        log_info("Đóng trình duyệt Chrome")
                                        driver.quit()

                                        log_info("Kết thúc tiến trình")
                                        return        
                    except TimeoutException:
                        bot_reply(user_id, "Thông báo sau khi click vào nút tắt live không xuất hiện trong thời gian chờ quy định")
                        bot_reply(user_id, f"Làm mới lại trang web")

                        log_error("Thông báo khi tắt live không xuất hiện trong thời gian chờ quy định, làm mới lại trang web")

                        # Cho làm mới lại trang web
                        driver.refresh()

                        # Kiểm tra xem có làm mới lại trang web livestream thành công hay không
                        try:
                            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

                            bot_reply(user_id, "Làm mới trang web livestream thành công")
                            log_success("Làm mới trang web thành công")
                        except TimeoutError:
                            bot_reply(user_id, "Làm mới trang web thất bại, xảy ra sự cố kết nối internet")
                            log_error("Làm mới trang web thất bại, xảy ra sự cố kết nối internet")

                            log_info("Đóng trình duyệt Chrome")
                            driver.quit()

                            log_info("Kết thúc tiến trình")
                            return
            except TimeoutException:
                # Kiểm tra phần tử Trạng thái và đưa ra kết luận cuối cùng
                try:
                    # Đợi phần tử Trạng thái xuất hiện
                    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.text-center:nth-child(10)')))

                    # Lấy dữ liệu của phần tử Trạng thái
                    dulieu_trangthai = driver.find_element(By.CSS_SELECTOR, "td.text-center:nth-child(10)").text

                    if dulieu_trangthai == "Mới":
                        bot_reply(user_id, f"Nút Dừng live không xuất hiện, Trạng thái luồng live là: {dulieu_trangthai}. Bạn có thể khởi tạo luồng live mới ngay bây giờ")
                        log_info("Hiện không có phiên live nào được mở")

                        log_info("Đóng trình duyệt chrome")
                        driver.quit()

                        log_info("Kết thúc tiến trình")
                        return
                except TimeoutException:
                    bot_reply(user_id, "Nút dừng live không xuất hiện, hiện tại luồng live đang trống, có thể khởi tạo phiên live mới ngay bây giờ")
                    log_info("Hiện không có phiên live nào được mở")

                    log_info("Đóng trình duyệt chrome")
                    driver.quit()

                    log_info("Kết thúc tiến trình")
                    return

    elif message.text in ["Không", "Trở lại menu chính"]:
        trolai_menuchinh(message)