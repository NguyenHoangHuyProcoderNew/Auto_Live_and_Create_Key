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
    # Nhập hàm đóng trình duyệt Chrome driver cũ
    from Moudles_support.support_chrome_driver import dong_chromedriver_cu
    from Moudles_support.support_bot import id_tiktok_vanbao, chon_taikhoan_vanbao, chon_taikhoan_meme, chon_taikhoan_nickphulbh, hoichieu_cu, quynhem_chui, nammod, tieudelive, id_tiktok_meme, id_tiktok_nickphulbh, hoichieu_moi, kenhchinh_quynhem

    id_tiktok = id_tiktok_vanbao
    chon_taikhoan_taocauhinhmoi = chon_taikhoan_vanbao

    # Kiểm tra sự lựa chọn mà người dùng đã chọn ở hàm Chọn Nguồn Cho Phiên Live
    if message.text == "Hồi Chiêu Cũ":
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn HỒI CHIÊU CŨ")
        log_info(f"Người dùng đã chọn nguồn live HỒI CHIÊU")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        linknguon = hoichieu_cu
    elif message.text == "Quỳnh Em Bản Full HD":
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn QUỲNH EM FULL HD")
        log_info("Tiến hành mở phiên live với nguồn QUỲNH EM FULL HD")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        linknguon = quynhem_chui
    elif message.text == "Kênh Chính Nam Mod":
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn Kênh Chính Nam Mod")
        log_info("Người dùng đã chọn nguồn live Kênh Chính Nam Mod")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        linknguon = nammod
    elif message.text == "Hồi Chiêu Mới":
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn Hồi Chiêu Mới")
        log_info("Tiến hành mở phiên live với nguồn Hồi Chiêu Mới")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        linknguon = hoichieu_moi
    elif message.text == "Kênh chính QUỲNH EM":
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn Kênh Chính Quỳnh Em")
        log_info("Tiến hành mở phiên live với nguồn Kênh Chính Quỳnh Em")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        linknguon = kenhchinh_quynhem
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

    dong_chromedriver_cu(message) # Chạy hàm đóng các phiên trình duyệt Chrome driver cũ
    
    # Khởi tạo Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Mở trang web livestream
    try:
        driver.get("https://autolive.me/tiktok")

        # Chờ tối đa 100 giây để đợi phần tử XPATCH được chỉ định xuất hiện, để đảm bảo trang web livestream đã tải hoàn tất
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b'))
        )

        bot_reply(user_id, "Truy cập trang web livestream thành công")
        log_success("Truy cập trang web livestream thành công")

        # Xóa cấu hình cũ
        bot_reply(user_id, "Tiến hành xóa luồng live hiện tại")

        # Kiểm tra xem có xóa cấu hình cũ thành công hay không
        try:
            log_info("Click vào nút xóa luồng live")
            driver.find_element(By.XPATH, '//button[@class="btn btn-circle btn-dark btn-sm waves-effect waves-light btn-status-live" and @data-status="-1" and @data-toggle="tooltip"]').click()

            # Chờ tối đa 100 giây để đợi thông báo xuất hiện sau khi click vào nút "Xóa luồng live"
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

            # Lấy nội dung của thông báo xóa luồng live cũ
            thongbao_xoaluonglive_cu = driver.execute_script('''
                // JavaScript code here
                // Đoạn mã JavaScript để lấy nội dung của phần tử
                var element = document.querySelector('div.text[data-notify-html="text"]');
                return element.textContent;
            ''')

            # Kiểm tra nội dung của thông báo xóa luồng live cũ
            if thongbao_xoaluonglive_cu == "Success":
                bot_reply(user_id, "Xoá luồng live cũ thành công")
                log_success(f"Xoá luồng live cũ thành công - Thông báo của web: {thongbao_xoaluonglive_cu}")
            else:
                bot_reply(user_id, f"Xoá luồng live cũ thất bại - Thông báo từ web: {thongbao_xoaluonglive_cu}")
                log_error(f"Xóa luồng live cũ thất bại - Thông báo từ web: {thongbao_xoaluonglive_cu}")

                log_info("Đóng trình duyệt Chrome")
                driver.quit()

                log_info("Kết thúc tiến trình")
                return
        except NoSuchElementException:
            bot_reply(user_id, "Hiện tại không có cấu hình cũ")
            log_info("Không tìm thấy nút xoá cấu hình live trên trang web => Hiện tại không có luồng live nào")

        # Khởi tạo luồng live mới
        bot_reply(user_id, "Khởi tạo luồng live mới")
        log_info("Khởi tạo luồng live mới")

        log_info("Đang chọn tài khoản live")
        driver.find_element(By.CSS_SELECTOR, f"{chon_taikhoan_taocauhinhmoi}").click()

        log_info("Đang nhập tiêu đề live")
        driver.find_element(By.ID, "title").send_keys(tieudelive)

        log_info("Đang chọn chủ đề live")
        driver.find_element(By.CSS_SELECTOR, "#topic > option:nth-child(11)").click()

        log_info("Đang chọn kiểu live")
        driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(6) > div > div > div > button:nth-child(2) > i").click()

        log_info("Đang nhập link nguồn cho phiên live")
        driver.find_element(By.ID, "url_source").send_keys(linknguon)

        # Lưu luồng live mới sau khi khởi tạo
        bot_reply(user_id, "Khởi tạo luồng live hoàn tất, tiến hành lưu lại luồng live")
        log_info("Lưu luồng live mới")

        # Kiểm tra xem có lưu luồng live thành công hay không
        try:
            log_info("Click vào nút lưu luồng live")
            driver.find_element(By.CSS_SELECTOR, "#formLive > button").click()

            log_info("Làm mới lại trang web để lưu luồng live")
            driver.refresh()

            # Chờ tối đa 100 giây để đợi phần tử XPATCH được chỉ định xuất hiện, để đảm bảo trang web livestream đã tải hoàn tất
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))

            bot_reply(user_id, "Lưu luồng live thành công")
            log_success("Làm mới trang web livestream thành công, luồng live đã được lưu lại")

            # Mở phiên live lần 1
            bot_reply(user_id, "Tiến hành mở phiên live")
            log_info("Mở phiên live lần 1")

            # Kiểm tra sự xuất hiện của nút Bắt đầu live và mở phiên live trong lần 1
            try:
                # Chờ tối đa 10 giây để đợi nút "Bắt đầu live" xuất hiện lần 1
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']"))
                )

                # Click vào nút "Bắt đầu live" lần 1
                log_info("Click vào nút Bắt đầu live")
                driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

                # Kiểm tra xem có mở phiên live thành công hay không trong lần 1
                try:
                    # Chờ tối đa 100 giây để đợi thông báo xuất hiện sau khi click vào nút "Bắt đầu live"
                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

                    # Lấy nội dung của thông báo mở live lần 1
                    thongbao_molive_lan1 = driver.execute_script('''
                        // JavaScript code here
                        // Đoạn mã JavaScript để lấy nội dung của phần tử
                        var element = document.querySelector('div.text[data-notify-html="text"]');
                        return element.textContent;
                    ''')

                    # Kiểm tra nội dung của thông báo mở live lần 1
                    if thongbao_molive_lan1 == "Success":
                        bot_reply(user_id, "Mở phiên live thành công")
                        log_info(f"Thông báo của web là {thongbao_molive_lan1} - Mở live thành công")

                        # Truy cập vào phiên live để  kiểm tra thời điểm phiên live được mở lần 1
                        bot_reply(user_id, "Tiến hành truy cập vào phiên live để kiểm tra thời điểm phiên live được mở")
                        log_info("Truy cập vào phiên live để kiểm tra thời điểm phiên live được mở")

                        # Kiểm tra xem có truy cập phiên live thành công hay không lần 1
                        try:
                            # Mở trang web livestream
                            driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

                            # Chờ tối đa 100 giây để XPATCH được chỉ định xuất hiện, để đảm bảo rằng phiên live đã tải hoàn tất lần 1
                            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                            bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
                            log_success("Truy cập phiên live thành công => TIẾN HÀNH KIỂM TRA THỜI ĐIỂM PHIÊN LIVE ĐƯỢC MỞ")

                            # Vòng lặp whilte lặp lại việc kiểm tra số lượng người xem của phiên live cho đến khi nào phiên live được diễn ra thì mới kết thúc vòng lặp lần 1
                            while True:
                                now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống
                                try:
                                    # Đợi tối đa 10 giây để XPATCH chứa dữ liệu là số lượng người xem của phiên live xuất hiện rồi mới kiểm tra
                                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
                                    
                                    bot_reply(user_id, f"Check live hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                                    log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

                                    log_info("Đóng trình duyệt chrome")
                                    driver.quit()

                                    log_info("Kết thúc tiến trình")
                                    return
                                except TimeoutException:
                                    log_error("Phiên live chưa được diễn ra")
                                    log_info("Làm mới lại phiên live")

                                    # Làm mới lại phiên live
                                    driver.refresh()

                                    # Kiểm tra xem có làm mới lại phiên live thành công hay không
                                    try:
                                        # Chờ tối đa 100 giây để XPATCH được chỉ định xuất hiện, để đảm bảo rằng phiên live đã tải hoàn tất
                                        WebDriverWait(driver, 100).until(
                                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                                        )
                                    except TimeoutException:
                                        bot_reply(user_id, "Kiểm tra phiên live thất bại, không thể tải phiên live trong thời gian chờ quy định")
                                        log_error("Kiểm tra phiên live thất bại, không thể tải phiên live trong thời gian chờ quy định")

                                        log_info("Đóng trình duyệt chrome")
                                        driver.quit()

                                        log_info("Kết thúc tiến trình")
                                        return
                        except TimeoutError:
                            bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
                            log_info("Không thể truy cập phiên live do kết nối internet")

                            log_info("Đóng trình duyệt chrome")
                            driver.quit()

                            log_info("Kết thúc tiến trình")
                            return
                    else:
                        bot_reply(user_id, f"Mở phiên live thất bại\nThông báo từ web: {thongbao_molive_lan1}")
                        log_error(f"Mở phiên live thất bại - Thông báo từ web: {thongbao_molive_lan1}")

                        driver.quit()
                        log_info("Đóng trình duyệt chrome")

                        log_info("Kết thúc tiến trình")
                        return
                except TimeoutError:
                    bot_reply(user_id, "Mở phiên live thất bại, thông báo mở phiên live không xuất hiện trong thời gian chờ")
                    log_error("Mở phiên live thất bại, thông báo mở phiên live không xuất hiện trong thời gian chờ")
            except TimeoutException:
                bot_reply(user_id, "Nút Bắt đầu live không xuất hiện lần 1")
                log_error("Không tồn tại nút Bắt đầu live lần 1")

                bot_reply(user_id, "Làm mới lại trang web livestream để kiểm tra sự xuất hiện của nút Bắt đầu live lần 2")
                log_info("Làm mới lại trang web livestream")

                driver.refresh() # Làm mới lại trang web livestream

                # Kiểm tra xem có làm mới lại trang web livestream thành công hay không để kiểm tra sự xuất hiện của nút Bắt đầu live lần 2
                try:
                    # Chờ tối đa 100 giây để đợi phần tử XPATCH được chỉ định xuất hiện, để đảm bảo trang web livestream đã làm mới hoàn tất
                    WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b'))
                    )

                    bot_reply(user_id, "Làm mới lại trang web livestream thành công")
                    log_success("Làm mới lại trang web livestream thành công để kiểm tra sự xuất hiện của nút Bắt đầu live lần 2")

                    # Kiểm tra sự xuất hiện của nút bắt đầu live lần 2
                    try:
                        # Chờ tối đa 10 giây để đợi nút "Bắt đầu live" xuất hiện lần 2
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']"))
                        )

                        bot_reply(user_id, "Nút bắt đầu live đã xuất hiện trong lần kiểm tra thứ 2")
                        bot_reply("Tiến hành mở phiên live")

                        # Click vào nút "Bắt đầu live" lần 2
                        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

                        # Lấy nội dung của thông báo "Bắt đầu live" lần 2
                        thongbao_molive_lan2 = driver.execute_script('''
                            // JavaScript code here
                            // Đoạn mã JavaScript để lấy nội dung của phần tử
                            var element = document.querySelector('div.text[data-notify-html="text"]');
                            return element.textContent;
                        ''')

                        if thongbao_molive_lan2 == "Success":
                            bot_reply("Mở phiên live thành công")
                            log_info(f"Thông báo của web là {thongbao_molive_lan1} - Mở live thành công")

                            # Truy cập vào phiên live để  kiểm tra thời điểm phiên live được mở lần 2
                            bot_reply(user_id, "Tiến hành truy cập vào phiên live để kiểm tra thời điểm phiên live được mở")
                            log_info("Truy cập vào phiên live để kiểm tra thời điểm phiên live được mở")

                            # Kiểm tra xem có truy cập phiên live thành công hay không lần 2
                            try:
                                # Mở trang web livestream
                                driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

                                # Chờ tối đa 100 giây để XPATCH được chỉ định xuất hiện, để đảm bảo rằng phiên live đã tải hoàn tất lần 1
                                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                                bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
                                log_success("Truy cập phiên live thành công => TIẾN HÀNH KIỂM TRA THỜI ĐIỂM PHIÊN LIVE ĐƯỢC MỞ")

                                # Vòng lặp whilte lặp lại việc kiểm tra số lượng người xem của phiên live cho đến khi nào phiên live được diễn ra thì mới kết thúc vòng lặp lần 1
                                while True:
                                    now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống
                                    try:
                                        # Đợi tối đa 10 giây để XPATCH chứa dữ liệu là số lượng người xem của phiên live xuất hiện rồi mới kiểm tra
                                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
                                        
                                        bot_reply(user_id, f"Check live hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                                        log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

                                        log_info("Đóng trình duyệt chrome")
                                        driver.quit()

                                        log_info("Kết thúc tiến trình")
                                        return
                                    except TimeoutException:
                                        log_error("Phiên live chưa được diễn ra")
                                        log_info("Làm mới lại phiên live")

                                        # Làm mới lại phiên live
                                        driver.refresh()

                                        # Kiểm tra xem có làm mới lại phiên live thành công hay không
                                        try:
                                            # Chờ tối đa 100 giây để XPATCH được chỉ định xuất hiện, để đảm bảo rằng phiên live đã tải hoàn tất
                                            WebDriverWait(driver, 100).until(
                                                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                                            )
                                        except TimeoutException:
                                            bot_reply(user_id, "Kiểm tra phiên live thất bại, không thể tải phiên live trong thời gian chờ quy định")
                                            log_error("Kiểm tra phiên live thất bại, không thể tải phiên live trong thời gian chờ quy định")

                                            log_info("Đóng trình duyệt chrome")
                                            driver.quit()

                                            log_info("Kết thúc tiến trình")
                                            return
                            except TimeoutError:
                                bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
                                log_info("Không thể truy cập phiên live do kết nối internet")

                                log_info("Đóng trình duyệt chrome")
                                driver.quit()

                                log_info("Kết thúc tiến trình")
                                return
                        else:
                            bot_reply(user_id, f"Mở phiên live thất bại\nThông báo từ web: {thongbao_molive_lan1}")
                            log_error(f"Mở phiên live thất bại - Thông báo từ web: {thongbao_molive_lan1}")

                            driver.quit()
                            log_info("Đóng trình duyệt chrome")

                            log_info("Kết thúc tiến trình")
                            return
                    except TimeoutException:
                        bot_reply(user_id, "Nút Bắt đầu live vẫn không xuất hiện trong lần kiểm tra thứ 2, vui lòng truy cập vào trang web và kiểm tra lại")
                        log_error("Không tồn tại nút mở live lần 2")

                        log_info("Đóng trình duyệt Chrome")
                        driver.quit()

                        log_info("Kết thúc tiến trình")
                        return
                except TimeoutError:
                    bot_reply(user_id, "làm mới lại trang web livestream thất bại, trong lần kiểm tra sự xuất hiện của nút Bắt đầu live lần 2")
                    log_error("làm mới lại trang web livestream thất bại, trong lần kiểm tra sự xuất hiện của nút Bắt đầu live lần 2")

                    log_info("Đóng trình duyệt Chrome")
                    driver.quit()

                    log_info("Kết thúc tiến trình")
                    return
        except TimeoutError:
            bot_reply(user_id, "Lưu luồng live thất bại, xảy ra sự cố kết nối internet")
            log_error("Lưu luồng live thất bại, xảy ra sự cố kết nối internet")

            log_info("Đóng trình duyệt Chrome")
            driver.quit()

            log_info("Kết thúc tiến trình")
            return
    except TimeoutError:
        bot_reply(user_id, "Truy cập trang web livestream thất bại, xảy ra sự cố kết nối internet")
        log_error("Không thể truy cập trang web livestream, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return