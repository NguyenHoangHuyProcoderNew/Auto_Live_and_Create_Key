import datetime
from colorama import Fore, Style, init

# Khởi tạo colorama
init()

# Định nghĩa màu xanh dương nhạt
LIGHT_BLUE = '\033[94m'

def get_current_time():
    """Trả về giờ:phút:giây hiện tại của hệ thống"""
    now = datetime.datetime.now()
    return now.strftime('%H:%M:%S')

def log_info(message):
    """In log với thông báo INFO"""
    time_str = get_current_time()
    print(f"{LIGHT_BLUE}[{time_str}]{Style.RESET_ALL} {Fore.YELLOW}[INFO]{Style.RESET_ALL} {message}")

def log_success(message):
    """In log với thông báo SUCCESS"""
    time_str = get_current_time()
    print(f"{LIGHT_BLUE}[{time_str}]{Style.RESET_ALL} {Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")    

def log_warning(message):
    """In log với thông báo WARNING"""
    time_str = get_current_time()
    print(f"{LIGHT_BLUE}[{time_str}]{Style.RESET_ALL} {Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}")

def log_error(message):
    """In log với thông báo ERROR"""
    time_str = get_current_time()
    print(f"{LIGHT_BLUE}[{time_str}]{Style.RESET_ALL} {Fore.RED}[ERROR]{Style.RESET_ALL} {message}")