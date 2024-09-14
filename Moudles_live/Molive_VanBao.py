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

# Trở lại menu chính
def trolai_menuchinh(message):
    nut_menuchinh = telebot.types.ReplyKeyboardMarkup(True).add('Mở live', 'Tắt live', 'Đổi IP').add('Trở về menu chính')
    bot.send_message(message.chat.id, "VUI LÒNG CHỌN 👇", reply_markup=nut_menuchinh)

# Yêu cầu người dùng chọn nguồn cho phiên live 
def chon_nguon_chophienlive_vanbao(message):
    # Tạo nút chọn nguồn cho phiên live
    nut_chon_nguon_chophienlive = types.ReplyKeyboardMarkup(True).add('Hồi Chiêu', 'Quỳnh Em', 'Nam Mod').add('Trở lại menu chính')
    bot.send_message(message.chat.id, "Bạn muốn sử dụng nguồn live nào cho phiên live?", reply_markup=nut_chon_nguon_chophienlive)
    log_info("Đang yêu cầu người dùng chọn nguồn cho phiên live")
    
    bot.register_next_step_handler(message, xuly_molive_vanbao)

# Xử lý việc mở live
def xuly_molive_vanbao(message):
    """"Nhập chức năng đóng toàn bộ trình duyệt Chrome trước khi khởi tạo Chrome driver mới"""
    from Moudles_support.support_chrome_driver import dong_toanbo_trinhduyet_chrome

    id_tiktok = "vanbao165201"
    chon_taikhoan_taocauhinhmoi = "#tiktok_account > option:nth-child(6)"

    # Kiểm tra sự lựa chọn mà người dùng đã chọn ở hàm Chọn Nguồn Cho Phiên Live
    if message.text == "Hồi Chiêu":
        linknguon = "https://drive.google.com/file/d/1PrRqUCTGm0nseYKJwARZYuCmsxMc-T7k/view?usp=drivesdk" # NGUỒN HỒI CHIÊU
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn HỒI CHIÊU")
        log_info(f"Người dùng đã chọn nguồn live HỒI CHIÊU")
    elif message.text == "Quỳnh Em":
        linknguon = "https://drive.google.com/file/d/1IyXrUXOJGvzPrxxgP7W0oX0ONJciesdo/view?usp=drivesdk" # NGUỒN QUỲNH EM
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn QUỲNH EM")
        log_info("Tiến hành mở phiên live với nguồn QUỲNH EM")
    elif message.text == "Nam Mod":
        linknguon = "https://www.tiktok.com/@trumkeoranknammod/live"
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn Nam Mod")
        log_info("Người dùng đã chọn nguồn live Nam Mod")
    elif message.text == "Trở lại menu chính":
        log_info(f"Người dùng đã chọn Trở lại menu chính")
        trolai_menuchinh(message)
        return
    else:
        bot_reply(user_id, "Lựa chọn không hợp lệ")
        trolai_menuchinh(message)
        log_error("Lựa chọn không hợp lệ - trở về menu chính")
        return
    
    # Gọi chức năng đóng trình duyệt Chrome driver cũ
    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome driver cũ")
    log_info("Chạy hàm đóng các phiên trình duyệt Chrome driver cũ")

    dong_toanbo_trinhduyet_chrome(message) # Chạy hàm đóng các phiên trình duyệt Chrome driver cũ

    # Khởi tạo Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Xử lý toàn bộ quá trình mở phiên live
    try:
        bot_reply(user_id, "Mở trang web livestream")
        log_info("Truy cập vào trang web livestream")

        # Mở trang web livestream
        driver.get('https://autolive.one/tiktok')

        # Đợi phần tử của trang web xuất hiện
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        bot_reply(user_id, "Mở trang web livestream thành công")
        log_success("Truy cập vào trang web thành công")

        # Xoá cấu hình hiện tại trước khi khởi tạo luồng live mới
        bot_reply(user_id, "Tiến hành xoá luồng live cũ")
        log_info("Xoá cấu hình live hiện tại")

        # Xử lý quá trình xoá cấu hình hiện tại
        try:
            # Click vào nút xoá cấu hình
            driver.find_element(By.XPATH, '//button[@class="btn btn-circle btn-dark btn-sm waves-effect waves-light btn-status-live" and @data-status="-1" and @data-toggle="tooltip"]').click()

            # Đợi thông báo từ web sau khi xoá cấu hình
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

            # Lấy nội dung của thông báo
            thongbao_xoacauhinhcu = driver.execute_script('''
            // JavaScript code here
            // Đoạn mã JavaScript để lấy nội dung của phần tử
            var element = document.querySelector('div.text[data-notify-html="text"]');
            return element.textContent;
        ''')

            # Kiểm tra dữ liệu của thông báo sau khi xoá cấu hình cũ
            if thongbao_xoacauhinhcu == "Success":
                bot_reply(user_id, "Xoá luồng live cũ thành công")
                log_success(f"Xoá luồng live cũ thành công - Thông báo của web: {thongbao_xoacauhinhcu}")
            else:
                bot_reply(user_id, f"Xoá luồng live cũ thất bại - Thông báo từ web: {thongbao_xoacauhinhcu}")
                log_error(f"Xóa luồng live cũ thất bại - Thông báo từ web: {thongbao_xoacauhinhcu}")

                log_info("Đóng trình duyệt Chrome")
                driver.quit()

                log_info("Kết thúc tiến trình")
                return
        except NoSuchElementException:
            bot_reply(user_id, "Hiện tại không có luồng live nào")
            log_info("Không tìm thấy nút xoá cấu hình live trên trang web => Hiện tại không có luồng live nào")

        # Khởi tạo luồng live mới
        bot_reply(user_id, "Khởi tạo luồng live mới")
        log_info("Khởi tạo luồng live mới")

        log_info("Đang chọn tài khoản live")
        driver.find_element(By.CSS_SELECTOR, f"{chon_taikhoan_taocauhinhmoi}").click()

        log_info("Đang nhập tiêu đề live")
        driver.find_element(By.ID, "title").send_keys('kéo rank Liên Quân')

        log_info("Đang chọn chủ đề live")
        driver.find_element(By.CSS_SELECTOR, "#topic > option:nth-child(11)").click()

        log_info("Đang chọn kiểu live")
        driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(6) > div > div > div > button:nth-child(2) > i").click()

        log_info("Đang nhập link nguồn cho phiên live")
        driver.find_element(By.ID, "url_source").send_keys(linknguon)

        # Lưu luồng live mới sau khi khởi tạo
        bot_reply(user_id, "Khởi tạo luồng live hoàn tất, tiến hành lưu lại luồng live")
        log_info("Lưu luồng live mới")

        # Kiểm tra xem có lưu luồng live thành công hay không
        try:
            log_info("Click vào nút lưu luồng live")
            driver.find_element(By.CSS_SELECTOR, "#formLive > button").click()

            log_info("Làm mới lại trang web để lưu luồng live")
            driver.refresh()

            # Kiểm tra xem có làm mới lại trang web thành công hay không
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))

            bot_reply(user_id, "Lưu luồng live mới thành công")
            log_info("Làm mới trang web hoàn tất - luồng live đã được lưu lại")

            # Mở phiên live sau khi lưu luồng live thành công
            bot_reply(user_id, "Tiến hành mở phiên live")
            log_info("Mở phiên live")

            # Xử lý quá trình mở phiên live lần 1
            try:
                # Đợi nút mở phiên live xuất hiện
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']"))
                )

                bot_reply(user_id, "Nút Bắt đầu live đã xuất hiện")
                log_success("Nút Bắt đầu live đã xuất hiện")

                # Click vào nút "Bắt đầu live" để mở phiên live
                driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

                bot_reply(user_id, "Click vào nút Bắt đầu live thành công, đang đợi thông báo từ web...")
                log_success("Click vào nút Bắt đầu live thành công, đang đợi thông báo từ web")

                # Kiểm tra xem có mở phiên live thành công hay không
                try:
                    # Đợi thông báo của web xuất hiện sau khi click vào nút "Bắt đầu live"
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

                    # Lấy nội dung của thông báo
                    thongbao_batdaulive = driver.execute_script('''
                        // JavaScript code here
                        // Đoạn mã JavaScript để lấy nội dung của phần tử
                        var element = document.querySelector('div.text[data-notify-html="text"]');
                        return element.textContent;
                    ''')
                    
                    # Kiểm tra thông báo từ web
                    if thongbao_batdaulive == "Success":
                        bot_reply(user_id, "Mở live thành công")
                        log_info(f"Thông báo của web là {thongbao_batdaulive} - Mở live thành công")

                        # Truy cập vào phiên live sau khi mở live thành công để kiểm tra thời điểm phiên live được mở
                        bot_reply(user_id, "Truy cập vào phiên live")
                        log_error("Truy cập vào phiên live để kiểm tra thời điểm phiên live được diễn ra")
                        try:
                            # Truy cập vào phiên live
                            driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

                            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                            bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
                            log_success("Truy cập vào phiên live thành công => TIẾN HÀNH KIỂM TRA")

                            # Kiểm tra thời điểm phiên live được mở
                            while True:
                                now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống
                                try:
                                    # Đợi 10 giây để phần tử chứa số lượng người xem xuất hiện
                                    checkview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
                                    
                                    bot_reply(user_id, f"Kiểm tra hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                                    log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

                                    log_info("Đóng trình duyệt chrome")
                                    driver.quit()

                                    log_info("Kết thúc tiến trình")
                                    return
                                except TimeoutException:
                                    log_info("Phiên live chưa được diễn ra")

                                    log_info("Làm mới lại phiên live")
                                    driver.refresh()

                                    # Kiểm tra xem có làm mới lại phiên live thành công hay không
                                    try:
                                        WebDriverWait(driver, 100).until(
                                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                                        )
                                    except TimeoutError:
                                        bot_reply(user_id, "Kiểm tra phiên live thất bại do có sự cố kết nối internet, vui lòng kiểm tra lại đường truyền")
                                        log_error("Kiểm tra phiên live thất bại do có sự cố về kết nối internet")

                                        log_info("Đóng trình duyệt chrome")
                                        driver.quit()

                                        log_info("Kết thúc tiến trình")
                                        return
                        except TimeoutError:
                            bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
                            log_info("Truy cập phiên live thất bại, xảy ra sự cố kết nối internet")

                            log_info("Đóng trình duyệt Chrome")
                            driver.quit()

                            log_info("Kết thúc tiến trình")
                            return
                    else:
                        bot_reply(user_id, f"Mở live thất bại\nThông báo từ web: {thongbao_batdaulive}")
                        log_error(f"Mở phiên live thất bại - Thông báo từ web: {thongbao_batdaulive}")

                        driver.quit()
                        log_info("Đóng trình duyệt chrome")

                        log_info("Kết thúc tiến trình")
                        return
                except TimeoutException:
                    bot_reply(user_id, "Thông báo của web không xuất hiện trong thời gian chờ")
                    log_error("Thông báo không xuất hiện trong thời gian chờ quy định")

                    # Lặp lại việc bật live cho đến khi nào phiên live được mở thì thôi
                    while True:
                        # Cho làm mới lại trang web khi thông báo không xuất hiện trong thời gian chờ quy định
                        bot_reply(user_id, "Làm mới lại trang web")
                        log_info("Làm mới lại trang web")

                        driver.refresh() # Làm mới lại trang web

                        # Kiểm tra xem có làm mới trang web livestream thành công hay không
                        try:
                            now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống

                            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

                            bot_reply(user_id, "Làm mới lại trang web livestram thành công")
                            log_success("Làm mới lại trang web livestream thành công")

                            """ Kiểm tra Trạng thái luồng live sau khi làm mới lại trang web """
                            bot_reply(user_id, "Tiến hành kiểm tra Trạng thái luồng live")
                            log_info("Kiểm tra Trạng thái luồng live sau khi làm mới lại trang web")

                            # Lấy dữ liệu của phần tử Trạng thái
                            trangthai_luonglive = driver.find_element(By.CSS_SELECTOR, "td.text-center:nth-child(10)").text

                            # Kiểm tra Trạng thái luồng live
                            if trangthai_luonglive == "Đang live":
                                bot_reply(user_id, f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Trạng thái luồng live là: {trangthai_luonglive}, phiên live đã được diễn ra")
                                log_success("Phiên live đã được mở")

                                log_info("Đóng trình duyệt Chrome")
                                driver.quit()

                                log_info("Kết thúc tiến trình")
                                return
                            elif "Đang download, dự kiến live lúc" in trangthai_luonglive:
                                bot_reply(user_id, "Luồng live đã được mở thành công")
                                bot_reply(user_id, "Truy cập vào phiên live")

                                log_success("Luồng live đã được mở, truy cập vào phiên live")

                                # Truy cập vào phiên live
                                driver.get(f"https://www.tiktok.com/@{id_tiktok}/live")

                                # Kiểm tra xem có truy cập vào phiên live thành công hay không
                                try:
                                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                                    bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
                                    log_success("Truy cập vào phiên live thành công => TIẾN HÀNH KIỂM TRA")

                                    # Kiểm tra thời điểm phiên live được mở
                                    while True:
                                        now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống

                                        # Xử lý kiểm tra thời điểm phiên live được mở
                                        try:
                                            # Đợi 10 giây để phần tử chứa số lượng người xem xuất hiện
                                            checkview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
                                            
                                            bot_reply(user_id, f"Kiểm tra hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                                            log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

                                            log_info("Đóng trình duyệt chrome")
                                            driver.quit()

                                            log_info("Kết thúc tiến trình")
                                            return
                                        except TimeoutException:
                                            log_info("Phiên live chưa được diễn ra")

                                            log_info("Làm mới lại phiên live")
                                            driver.refresh()

                                            # Kiểm tra xem có làm mới lại phiên live thành công hay không
                                            try:
                                                WebDriverWait(driver, 100).until(
                                                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                                                )
                                            except TimeoutException:
                                                bot_reply(user_id, "Kiểm tra phiên live thất bại do có sự cố kết nối internet, vui lòng kiểm tra lại đường truyền")
                                                log_error("Kiểm tra phiên live thất bại do có sự cố về kết nối internet")

                                                log_info("Đóng trình duyệt chrome")
                                                driver.quit()

                                                log_info("Kết thúc tiến trình")
                                                return
                                except TimeoutError:
                                    bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
                                    log_info("Truy cập phiên live thất bại, xảy ra sự cố kết nối internet")

                                    log_info("Đóng trình duyệt chrome")
                                    driver.quit()

                                    log_info("Kết thúc tiến trình")
                                    return            
                            elif trangthai_luonglive == "Mới":
                                # Click vào nút mở live
                                driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

                                # Kiểm tra xem có mở phiên live thành công hay không
                                try:
                                    # Đợi thông báo của web xuất hiện sau khi click vào nút "Bắt đầu live"
                                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

                                    # Lấy nội dung của thông báo
                                    thongbao_batdaulive = driver.execute_script('''
                                        // JavaScript code here
                                        // Đoạn mã JavaScript để lấy nội dung của phần tử
                                        var element = document.querySelector('div.text[data-notify-html="text"]');
                                        return element.textContent;
                                    ''')
                                    
                                    # Kiểm tra thông báo từ web
                                    if thongbao_batdaulive == "Success":
                                        bot_reply(user_id, "Mở live thành công")
                                        log_info(f"Thông báo của web là {thongbao_batdaulive} - Mở live thành công")

                                        # Truy cập vào phiên live sau khi mở live thành công để kiểm tra thời điểm phiên live được mở
                                        bot_reply(user_id, "Truy cập vào phiên live")
                                        log_error("Truy cập vào phiên live để kiểm tra thời điểm phiên live được diễn ra")
                                        try:
                                            # Truy cập vào phiên live
                                            driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

                                            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                                            bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
                                            log_success("Truy cập vào phiên live thành công => TIẾN HÀNH KIỂM TRA")

                                            # Kiểm tra thời điểm phiên live được mở
                                            while True:
                                                now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống
                                                try:
                                                    # Đợi 10 giây để phần tử chứa số lượng người xem xuất hiện
                                                    checkview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
                                                    
                                                    bot_reply(user_id, f"Kiểm tra hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                                                    log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

                                                    log_info("Đóng trình duyệt chrome")
                                                    driver.quit()

                                                    log_info("Kết thúc tiến trình")
                                                    return
                                                except TimeoutException:
                                                    log_info("Phiên live chưa được diễn ra")

                                                    log_info("Làm mới lại phiên live")
                                                    driver.refresh()

                                                    # Kiểm tra xem có làm mới lại phiên live thành công hay không
                                                    try:
                                                        WebDriverWait(driver, 100).until(
                                                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                                                        )
                                                    except TimeoutException:
                                                        bot_reply(user_id, "Kiểm tra phiên live thất bại do có sự cố kết nối internet, vui lòng kiểm tra lại đường truyền")
                                                        log_error("Kiểm tra phiên live thất bại do có sự cố về kết nối internet")

                                                        log_info("Đóng trình duyệt chrome")
                                                        driver.quit()

                                                        log_info("Kết thúc tiến trình")
                                                        return
                                        except TimeoutException:
                                            bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
                                            log_info("Truy cập phiên live thất bại, xảy ra sự cố kết nối internet")

                                            log_info("Đóng trình duyệt Chrome")
                                            driver.quit()

                                            log_info("Kết thúc tiến trình")
                                            return
                                    else:
                                        bot_reply(user_id, f"Mở live thất bại\nThông báo từ web: {thongbao_batdaulive}")
                                        log_error(f"Mở phiên live thất bại - Thông báo từ web: {thongbao_batdaulive}")

                                        driver.quit()
                                        log_info("Đóng trình duyệt chrome")

                                        log_info("Kết thúc tiến trình")
                                        return
                                except TimeoutException:
                                    bot_reply(user_id, "Thông báo của web không xuất hiện trong thời gian chờ")
                                    log_error("Thông báo không xuất hiện trong thời gian chờ quy định")
                        except TimeoutError:
                            bot_reply(user_id, "Làm mới lại trang web livestream thất bại, xảy ra sự cố kết nối intetnet")
                            log_error("Load trang web livestream thất bại")

                            log_info("Đóng trình duyệt chrome")
                            driver.quit()

                            log_info("Kết thúc tiến trình")
                            return
            except TimeoutException:
                bot_reply(user_id, "Nút Bắt đầu live không xuất hiện sau khi lưu luồng live mới")
                log_error("Không tồn tại nút mở live")

                # Làm mới lại trang web livestream sau khi lưu luồng live mà nút "Bắt đầu live" không xuất hiện
                bot_reply(user_id, "Làm mới lại trang web")
                log_info("Làm mới lại web")

                driver.refresh() # Làm mới lại trang web livestream

                # Kiểm tra xem có làm mới trang web livestream thành công hay không
                try:
                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

                    bot_reply(user_id, "Làm mới lại trang web livestram thành công")
                    log_success("Làm mới lại trang web livestream thành công")

                    # Kiểm tra sự tồn tại của nút "Bắt đầu live lần 2"
                    bot_reply(user_id, "Tiến hành kiểm tra sự tồn tại của nút Bắt đầu live lần 2")
                    log_info("Kiểm tra sự tồn tại của nút Bắt đầu live lần 2")

                    # Xử lý quá trình kiểm tra sự tồn tại của nút "Bắt đầu live" lần 2
                    try:
                        # Chờ nút "Bắt đầu live" xuất hiện
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']"))
                        )

                        bot_reply(user_id, "Kiểm tra hoàn tất, nút Bắt đầu live đã xuất hiện trong lần kiểm tra thứ 2")
                        log_success("Nút mở phiên live đã xuất hiện trong lần kiểm tra thứ 2")

                        bot_reply(user_id, "Tiến hành mở live")
                        log_info("Mở phiên live trong lần kiểm tra thứ 2")

                        """Mở live khi nút "Bắt đầu live đã xuất hiện trong lần kiểm tra thứ 2 """
                        # Kiểm tra xem có mở phiên live thành công hay không
                        try:
                            # Click vào nút mở phiên live
                            driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()
                            log_info("Click vào nút mở phiên live")
                            
                            # Đợi thông báo của web xuất hiện sau khi click vào nút "Bắt đầu live"
                            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

                            # Lấy nội dung của thông báo
                            thongbao_batdaulive = driver.execute_script('''
                            // JavaScript code here
                            // Đoạn mã JavaScript để lấy nội dung của phần tử
                            var element = document.querySelector('div.text[data-notify-html="text"]');
                            return element.textContent;
                        ''')
                            # Kiểm tra thông báo từ web
                            if thongbao_batdaulive == "Success":
                                bot_reply(user_id, "Mở live thành công")
                                log_info(f"Thông báo của web là {thongbao_batdaulive} - Mở live thành công")

                                # Truy cập vào phiên live sau khi mở live thành công để kiểm tra thời điểm phiên live được mở
                                bot_reply(user_id, "Truy cập vào phiên live")
                                log_error("Truy cập vào phiên live để kiểm tra thời điểm phiên live được diễn ra")
                                try:
                                    # Truy cập vào phiên live
                                    driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

                                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                                    bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
                                    log_success("Truy cập vào phiên live thành công => TIẾN HÀNH KIỂM TRA")

                                    # Kiểm tra thời điểm phiên live được mở
                                    while True:
                                        now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống
                                        try:
                                            # Đợi 10 giây để phần tử chứa số lượng người xem xuất hiện
                                            checkview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
                                            
                                            bot_reply(user_id, f"Kiểm tra hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                                            log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

                                            log_info("Đóng trình duyệt chrome")
                                            driver.quit()

                                            log_info("Kết thúc tiến trình")
                                            return
                                        except TimeoutException:
                                            log_info("Phiên live chưa được diễn ra")

                                            log_info("Làm mới lại phiên live")
                                            driver.refresh()

                                            # Kiểm tra xem có làm mới lại phiên live thành công hay không
                                            try:
                                                WebDriverWait(driver, 100).until(
                                                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                                                )
                                            except TimeoutException:
                                                bot_reply(user_id, "Kiểm tra phiên live thất bại do có sự cố kết nối internet, vui lòng kiểm tra lại đường truyền")
                                                log_error("Kiểm tra phiên live thất bại do có sự cố về kết nối internet")

                                                log_info("Đóng trình duyệt chrome")
                                                driver.quit()
                            
                                                log_info("Kết thúc tiến trình")
                                                return
                                            
                                except TimeoutException:
                                    bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
                                    log_info("Truy cập phiên live thất bại, xảy ra sự cố kết nối internet")

                                    log_info("Đóng trình duyệt Chrome")
                                    driver.quit()

                                    log_info("Kết thúc tiến trình")
                                    return
                            else:
                                bot_reply(user_id, f"Mở live thất bại\nThông báo từ web: {thongbao_batdaulive}")
                                log_error(f"Mở phiên live thất bại - Thông báo từ web: {thongbao_batdaulive}")

                                driver.quit()
                                log_info("Đóng trình duyệt chrome")

                                log_info("Kết thúc tiến trình")
                                return
                        except TimeoutException:
                            bot_reply(user_id, "Thông báo của web không xuất hiện trong thời gian chờ")
                            log_error("Thông báo không xuất hiện trong thời gian chờ quy định")

                            # Lặp lại việc bật live cho đến khi nào phiên live được mở thì thôi
                            while True:
                                # Cho làm mới lại trang web khi thông báo không xuất hiện trong thời gian chờ quy định
                                bot_reply(user_id, "Làm mới lại trang web")
                                log_info("Làm mới lại trang web")

                                driver.refresh() # Làm mới lại trang web

                                # Kiểm tra xem có làm mới trang web livestream thành công hay không
                                try:
                                    now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống

                                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

                                    bot_reply(user_id, "Làm mới lại trang web livestram thành công")
                                    log_success("Làm mới lại trang web livestream thành công")

                                    """ Kiểm tra Trạng thái luồng live sau khi làm mới lại trang web """
                                    bot_reply(user_id, "Tiến hành kiểm tra Trạng thái luồng live")
                                    log_info("Kiểm tra Trạng thái luồng live sau khi làm mới lại trang web")

                                    # Lấy dữ liệu của phần tử Trạng thái
                                    trangthai_luonglive = driver.find_element(By.CSS_SELECTOR, "td.text-center:nth-child(10)").text

                                    bot_reply(user_id, f"Trạng thái luồng live là: {trangthai_luonglive}")
                                    log_info(f"Trạng thái luồng live sau khi làm mới lại trang web là: {trangthai_luonglive}")

                                    # Kiểm tra Trạng thái luồng live
                                    if trangthai_luonglive == "Đang live":
                                        bot_reply(user_id, f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Trạng thái luồng live là: {trangthai_luonglive}, phiên live đã được diễn ra")
                                        log_success("Phiên live đã được mở")

                                        log_info("Đóng trình duyệt Chrome")
                                        driver.quit()

                                        log_info("Kết thúc tiến trình")
                                        return
                                    elif "Đang download, dự kiến live lúc" in trangthai_luonglive:
                                        bot_reply(user_id, "Luồng live đã được mở thành công")
                                        bot_reply("Truy cập vào phiên live")

                                        log_success("Luồng live đã được mở, truy cập vào phiên live")

                                        # Truy cập vào phiên live
                                        driver.get(f"https://www.tiktok.com/@{id_tiktok}/live")

                                        # Kiểm tra xem có truy cập vào phiên live thành công hay không
                                        try:
                                            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                                            bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
                                            log_success("Truy cập vào phiên live thành công => TIẾN HÀNH KIỂM TRA")

                                            # Kiểm tra thời điểm phiên live được mở
                                            while True:
                                                now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống

                                                # Xử lý kiểm tra thời điểm phiên live được mở
                                                try:
                                                    # Đợi 10 giây để phần tử chứa số lượng người xem xuất hiện
                                                    checkview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
                                                    
                                                    bot_reply(user_id, f"Kiểm tra hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                                                    log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

                                                    log_info("Đóng trình duyệt chrome")
                                                    driver.quit()

                                                    log_info("Kết thúc tiến trình")
                                                    return
                                                except TimeoutException:
                                                    log_info("Phiên live chưa được diễn ra")

                                                    log_info("Làm mới lại phiên live")
                                                    driver.refresh()

                                                    # Kiểm tra xem có làm mới lại phiên live thành công hay không
                                                    try:
                                                        WebDriverWait(driver, 100).until(
                                                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                                                        )
                                                    except TimeoutException:
                                                        bot_reply(user_id, "Kiểm tra phiên live thất bại do có sự cố kết nối internet, vui lòng kiểm tra lại đường truyền")
                                                        log_error("Kiểm tra phiên live thất bại do có sự cố về kết nối internet")

                                                        log_info("Đóng trình duyệt chrome")
                                                        driver.quit()

                                                        log_info("Kết thúc tiến trình")
                                                        return
                                        except TimeoutError:
                                            bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
                                            log_info("Truy cập phiên live thất bại, xảy ra sự cố kết nối internet")

                                            log_info("Đóng trình duyệt chrome")
                                            driver.quit()

                                            log_info("Kết thúc tiến trình")
                                            return            
                                    elif trangthai_luonglive == "Mới":
                                        # Click vào nút mở live
                                        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()
                                        bot_reply(user_id, "Click vào nút Bắt đầu live thành công, đang đợi thông báo từ web")
                                        log_info("Click vào nút Bắt đầu live sau khi làm mới lại trang web")

                                        # Kiểm tra xem có mở phiên live thành công hay không
                                        try:
                                            # Đợi thông báo của web xuất hiện sau khi click vào nút "Bắt đầu live"
                                            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

                                            # Lấy nội dung của thông báo
                                            thongbao_batdaulive = driver.execute_script('''
                                                // JavaScript code here
                                                // Đoạn mã JavaScript để lấy nội dung của phần tử
                                                var element = document.querySelector('div.text[data-notify-html="text"]');
                                                return element.textContent;
                                            ''')
                                            
                                            # Kiểm tra thông báo từ web
                                            if thongbao_batdaulive == "Success":
                                                bot_reply(user_id, "Mở live thành công")
                                                log_info(f"Thông báo của web là {thongbao_batdaulive} - Mở live thành công")

                                                # Truy cập vào phiên live sau khi mở live thành công để kiểm tra thời điểm phiên live được mở
                                                bot_reply(user_id, "Truy cập vào phiên live")
                                                log_error("Truy cập vào phiên live để kiểm tra thời điểm phiên live được diễn ra")
                                                try:
                                                    # Truy cập vào phiên live
                                                    driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

                                                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                                                    bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
                                                    log_success("Truy cập vào phiên live thành công => TIẾN HÀNH KIỂM TRA")

                                                    # Kiểm tra thời điểm phiên live được mở
                                                    while True:
                                                        now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống
                                                        try:
                                                            # Đợi 10 giây để phần tử chứa số lượng người xem xuất hiện
                                                            checkview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
                                                            
                                                            bot_reply(user_id, f"Kiểm tra hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                                                            log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

                                                            log_info("Đóng trình duyệt chrome")
                                                            driver.quit()

                                                            log_info("Kết thúc tiến trình")
                                                            return
                                                        except TimeoutException:
                                                            log_info("Phiên live chưa được diễn ra")

                                                            log_info("Làm mới lại phiên live")
                                                            driver.refresh()

                                                            # Kiểm tra xem có làm mới lại phiên live thành công hay không
                                                            try:
                                                                WebDriverWait(driver, 100).until(
                                                                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                                                                )
                                                            except TimeoutException:
                                                                bot_reply(user_id, "Kiểm tra phiên live thất bại do có sự cố kết nối internet, vui lòng kiểm tra lại đường truyền")
                                                                log_error("Kiểm tra phiên live thất bại do có sự cố về kết nối internet")

                                                                log_info("Đóng trình duyệt chrome")
                                                                driver.quit()

                                                                log_info("Kết thúc tiến trình")
                                                                return
                                                except TimeoutException:
                                                    bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
                                                    log_info("Truy cập phiên live thất bại, xảy ra sự cố kết nối internet")

                                                    log_info("Đóng trình duyệt Chrome")
                                                    driver.quit()

                                                    log_info("Kết thúc tiến trình")
                                                    return
                                            else:
                                                bot_reply(user_id, f"Mở live thất bại\nThông báo từ web: {thongbao_batdaulive}")
                                                log_error(f"Mở phiên live thất bại - Thông báo từ web: {thongbao_batdaulive}")

                                                driver.quit()
                                                log_info("Đóng trình duyệt chrome")

                                                log_info("Kết thúc tiến trình")
                                                return
                                        except TimeoutException:
                                            bot_reply(user_id, "Thông báo của web không xuất hiện trong thời gian chờ")
                                            log_error("Thông báo không xuất hiện trong thời gian chờ quy định")
                                except TimeoutError:
                                    bot_reply(user_id, "Làm mới lại trang web livestream thất bại, xảy ra sự cố kết nối intetnet")
                                    log_error("Load trang web livestream thất bại")

                                    log_info("Đóng trình duyệt chrome")
                                    driver.quit()

                                    log_info("Kết thúc tiến trình")
                                    return    
                    except TimeoutException:
                        bot_reply(user_id, "Kiểm tra lần 2 hoàn tất, nút Bắt đầu live vẫn không xuất hiện, vui lòng truy cập vào trang web và kiểm tra lại")
                        log_error("Không tồn tại nút mở live")
                        
                        log_info("Đóng trình duyệt chrome")
                        driver.quit()

                        log_info("Kết thúc tiến trình")
                        return
                except TimeoutError:
                    bot_reply(user_id, "Làm mới lại trang web livestream thất bại, xảy ra sự cố kết nối intetnet")
                    log_error("Load trang web livestream thất bại")

                    log_info("Đóng trình duyệt chrome")
                    driver.quit()

                    log_info("Kết thúc tiến trình")
                    return
        except TimeoutError:
            bot_reply(user_id, "Lưu luồng live thất bại, xảy ra sự cố kết nối internet")
            log_info("Lưu luồng live thất bại, xảy ra sự cố kết nối internet")

            driver.quit()
            log_info("Đóng trình duyệt Chrome")

            log_info("Kết thúc tiến trình")
            return
    except TimeoutError:
        bot_reply(user_id, "Mở trang web livestream thất bại, không thể tải được trang web trong thời gian chờ quy định. Xảy ra sự cố về kết nối internet")
        log_error("Truy cập vào trang web livestream thất bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return