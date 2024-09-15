import telebot

API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

user_id = "5634845912"

# Hàm thực hiện việc gửi tin nhắn cho người dùng
def bot_reply(user_id, message):
    # Gửi tin nhắn đến người dùng
    bot.send_message(user_id, message)

doiip_vanbao = "ip-23847"
doi_thietbi_vanbao = "renew-23847"
id_tiktok_vanbao = "vanbao165201"
chon_taikhoan_vanbao = "#tiktok_account > option:nth-child(3)"

doiip_nickphulbh = "ip-23848"
doi_thietbi_nickphulbh = "renew-23848"
id_tiktok_nickphulbh = "nammapsang_keorank"
chon_taikhoan_nickphulbh = "#tiktok_account > option:nth-child(4)"

doiip_meme = "ip-22733"
doi_thietbi_meme = "renew-22733"
id_tiktok_meme = "meme.l810"
chon_taikhoan_meme = "#tiktok_account > option:nth-child(2)"

hoichieu_fullhd = "https://drive.google.com/file/d/1PrRqUCTGm0nseYKJwARZYuCmsxMc-T7k/view?usp=drivesdk"
quynhem = "https://drive.google.com/file/d/1IyXrUXOJGvzPrxxgP7W0oX0ONJciesdo/view?usp=drivesdk"
nammod = "https://www.tiktok.com/@trumkeoranknammod/live"