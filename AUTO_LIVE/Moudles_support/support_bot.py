import telebot

API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

user_id = "5634845912"

# Hàm thực hiện việc gửi tin nhắn cho người dùng
def bot_reply(user_id, message):
    # Gửi tin nhắn đến người dùng
    bot.send_message(user_id, message)

doiip_tantai = "ip-23959"
doi_thietbi_tantai = "renew-23959"
id_tiktok_tantai = "tan_tai_hai_doi___"
chon_taikhoan_tantai = "#tiktok_account > option:nth-child(2)"

doiip_nickphulbh = "ip-23960"
doi_thietbi_nickphulbh = "renew-23960"
id_tiktok_nickphulbh = "nammapsang_keorank"
chon_taikhoan_nickphulbh = "#tiktok_account > option:nth-child(3)"

doiip_meme = "ip-23961"
doi_thietbi_meme = "renew-23961"
id_tiktok_meme = "meme.l810"
chon_taikhoan_meme = "#tiktok_account > option:nth-child(4)"

doiip_baohanstore = "ip-23967"
doi_thietbi_baohanstore = "renew-23967"
id_tiktok_baohanstore = "phuoc19903"
chon_taikhoan_baohanstore = "#tiktok_account > option:nth-child(6)"

doiip_chinhlbh = "ip-23969"
doi_thietbi_chinhlbh = "renew-23969"
id_tiktok_chinhlbh = "iam_huyle"
chon_taikhoan_chinhlbh = "#tiktok_account > option:nth-child(8)"



hoichieu_cu = "https://drive.google.com/file/d/1PrRqUCTGm0nseYKJwARZYuCmsxMc-T7k/view?usp=drivesdk"
hoichieu_moi = "https://drive.google.com/file/d/1lJQ6e_qmaMKY0SRf33_aUh1uthmHaUdp/view?usp=sharing"
quynhem_chui = "https://drive.google.com/file/d/1IyXrUXOJGvzPrxxgP7W0oX0ONJciesdo/view?usp=drivesdk"
nammod = "https://www.tiktok.com/@trumkeoranknammod/live"
kenhchinh_quynhem = "https://www.tiktok.com/@tytythanrien/live"

tieudelive = "kéo rank Liên Quân"
chonkieulive = "#formLive > div:nth-child(6) > div > div > div > button:nth-child(3)"