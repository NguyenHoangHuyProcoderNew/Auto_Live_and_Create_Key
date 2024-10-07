from selenium import webdriver
import os
import signal
import psutil

chromedriver_path = r'D:\\Chrome driver & du lieu bot auto\\chrome_driver\\chromedriver.exe'
dir = "D:\\Chrome driver & du lieu bot auto\\du lieu trinh duyet"

# Hàm tắt toàn bộ trình duyệt chrome trước khi khởi tạo chrome mới dành cho Mac OS
# def dong_chromedriver_cu(message):
#     try:
#         # Khởi tạo driver Chrome
#         driver = webdriver.Chrome()

#         # Lấy Process ID của trình duyệt Chrome do Selenium mở
#         chrome_pid = driver.service.process.pid

#         # Duyệt qua tất cả các process
#         for proc in psutil.process_iter(['pid', 'name']):
#             # Kiểm tra nếu process là 'chrome' và không phải là Selenium process
#             if proc.info['name'] == 'chrome' or proc.info['name'] == 'Google Chrome':
#                 if proc.info['pid'] != chrome_pid:
#                     # Gửi tín hiệu kết thúc cho process
#                     if os.name == 'nt':  # Windows
#                         proc.terminate()
#                     else:  # macOS
#                         os.kill(proc.info['pid'], signal.SIGTERM)

#         # Đóng trình duyệt do Selenium mở
#         driver.quit()

#     except Exception as e:
#         print(f"Error: {e}")

# Hàm tắt toàn bộ trình duyệt chrome trước khi khởi tạo chrome mới dành cho windows
def dong_chromedriver_cu(message):
    # Danh sách chỉ chứa chromedriver
    browser_names = ['chromedriver.exe']
    
    # Lấy danh sách PID của tất cả tiến trình chromedriver đang chạy
    chromedriver_pids = []
    
    # Tìm các tiến trình chromedriver.exe
    for process in psutil.process_iter():
        try:
            if process.name().lower() == 'chromedriver.exe':
                chromedriver_pids.append(process.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Tiến hành đóng các tiến trình chromedriver và các tiến trình con của nó
    for pid in chromedriver_pids:
        try:
            chromedriver_process = psutil.Process(pid)
            # Đóng chromedriver
            chromedriver_process.terminate()
            chromedriver_process.wait()

            # Đóng các tiến trình con (có thể là chrome.exe)
            for child in chromedriver_process.children(recursive=True):
                child.terminate()
                child.wait()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
