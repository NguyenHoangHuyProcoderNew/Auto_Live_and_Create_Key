from selenium import webdriver
import os
import signal
import psutil

# chromedriver_path = r'D:\\Chrome driver & du lieu bot auto\\chrome_driver\\chromedriver.exe'
# dir = "D:\\Chrome driver & du lieu bot auto\\du lieu trinh duyet"

chromedriver_path = '/Users/macx/Downloads/Chrome driver & du lieu trinh duyet/Chrome driver/chromedriver'
dir = "/Users/macx/Downloads/Chrome driver & du lieu trinh duyet/Du lieu trinh duyet"
# Hàm tắt toàn bộ trình duyệt chrome trước khi khởi tạo chrome mới dành cho Mac OS
def dong_chromedriver_cu(message):
    try:
        # Khởi tạo driver Chrome
        driver = webdriver.Chrome()

        # Lấy Process ID của trình duyệt Chrome do Selenium mở
        chrome_pid = driver.service.process.pid

        # Duyệt qua tất cả các process
        for proc in psutil.process_iter(['pid', 'name']):
            # Kiểm tra nếu process là 'chrome' và không phải là Selenium process
            if proc.info['name'] == 'chrome' or proc.info['name'] == 'Google Chrome':
                if proc.info['pid'] != chrome_pid:
                    # Gửi tín hiệu kết thúc cho process
                    if os.name == 'nt':  # Windows
                        proc.terminate()
                    else:  # macOS
                        os.kill(proc.info['pid'], signal.SIGTERM)

        # Đóng trình duyệt do Selenium mở
        driver.quit()

    except Exception as e:
        print(f"Error: {e}")

# Hàm tắt toàn bộ trình duyệt chrome trước khi khởi tạo chrome mới dành cho windows
def dong_chromedriver_cu(message):
    # Duyệt qua các process đang chạy
    for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            # Kiểm tra nếu process có liên quan đến chromedriver hoặc selenium
            if process.info['name'] == 'chrome.exe' or process.info['name'] == 'chromedriver.exe':
                cmdline = ' '.join(process.info['cmdline'])
                if '--remote-debugging-port' in cmdline:  # Chỉ ra rằng đây là một Chrome do Selenium mở
                    print(f"Đóng process: {process.info['pid']} - {cmdline}")
                    process.terminate()  # Hoặc dùng process.kill() nếu cần thiết
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# import subprocess

# def dong_chromedriver_cu(message):
#     try:
#         # Dùng lệnh `pkill` để tìm và giết tất cả các tiến trình liên quan đến chromedriver
#         subprocess.run(["pkill", "-f", "chromedriver"], check=True)
#         print("Đã đóng toàn bộ các tiến trình ChromeDriver.")
#     except subprocess.CalledProcessError as e:
#         print("Không thể đóng ChromeDriver:", e)
