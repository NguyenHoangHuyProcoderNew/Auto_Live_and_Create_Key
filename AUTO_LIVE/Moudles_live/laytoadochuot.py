import pyautogui
import time
import pyperclip  # Thư viện để sao chép nội dung vào clipboard

# Hàm đếm ngược theo số giây chờ được chỉ định
def dem_nguoc(seconds):
    while seconds > 0:
        print(f"Chờ {seconds} giây...", end="\r")  # In ra số giây chờ
        time.sleep(1)
        seconds -= 1

# Thời gian chờ (3 giây)
thoi_gian_cho = 3

# Thực hiện đếm ngược
dem_nguoc(thoi_gian_cho)

# Lấy tọa độ hiện tại của con trỏ chuột
x, y = pyautogui.position()
toa_do = f"{x}, {y}"
print(toa_do)

# Sao chép tọa độ vào clipboard
pyperclip.copy(toa_do)
print("Tọa độ đã được sao chép vào clipboard.")

# Kết thúc chương trình
print("Chương trình kết thúc.")
