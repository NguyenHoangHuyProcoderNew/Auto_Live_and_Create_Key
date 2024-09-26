import telebot

API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

user_id = "5634845912"

# Hàm thực hiện việc gửi tin nhắn cho người dùng
def bot_reply(user_id, message):
    # Gửi tin nhắn đến người dùng
    bot.send_message(user_id, message)

doiip_tantai = "ip-23865"
doi_thietbi_tantai = "renew-23865"
id_tiktok_tantai = "tan_tai_hai_doi___"
chon_taikhoan_tantai = "#tiktok_account > option:nth-child(5)"

doiip_nickphulbh = "ip-23848"
doi_thietbi_nickphulbh = "renew-23848"
id_tiktok_nickphulbh = "nammapsang_keorank"
chon_taikhoan_nickphulbh = "#tiktok_account > option:nth-child(4)"

doiip_meme = "ip-22733"
doi_thietbi_meme = "renew-22733"
id_tiktok_meme = "meme.l810"
chon_taikhoan_meme = "#tiktok_account > option:nth-child(2)"

hoichieu_cu = "https://drive.google.com/file/d/1PrRqUCTGm0nseYKJwARZYuCmsxMc-T7k/view?usp=drivesdk"
hoichieu_moi = "https://drive.google.com/file/d/1lJQ6e_qmaMKY0SRf33_aUh1uthmHaUdp/view?usp=sharing"
quynhem_chui = "https://drive.google.com/file/d/1IyXrUXOJGvzPrxxgP7W0oX0ONJciesdo/view?usp=drivesdk"
nammod = "https://www.tiktok.com/@trumkeoranknammod/live"
kenhchinh_quynhem = "https://www.tiktok.com/@tytythanrien/live"


tieudelive = ""
