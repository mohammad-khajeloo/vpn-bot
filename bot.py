import telebot
from telebot import types
import json
import os

TOKEN = "8574304496:AAHtGFJRmlOGwSDKM74iOtBr3zD866QdHXY"

CHANNEL_USERNAME = "@gostVpn37"

ADMIN_USERNAME = "gost_support37"

bot = telebot.TeleBot(TOKEN)

DB_FILE = "users.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start(message):

    user_id = str(message.from_user.id)

    args = message.text.split()

    users = load_users()

    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if member.status not in ['member', 'administrator', 'creator']:
            raise Exception()

    except:

        markup = types.InlineKeyboardMarkup()

        join_btn = types.InlineKeyboardButton(
            "📢 عضویت در کانال",
            url="https://t.me/gostVpn37"
        )

        markup.add(join_btn)

        bot.send_message(
            message.chat.id,
            "❌ ابتدا باید عضو کانال شوید",
            reply_markup=markup
        )

        return

    if user_id not in users:

        users[user_id] = {
            "coins": 0,
            "invited_by": None
        }

        if len(args) > 1:

            inviter_id = args[1]

            if inviter_id != user_id and inviter_id in users:

                users[user_id]["invited_by"] = inviter_id

                users[inviter_id]["coins"] += 1

        save_users(users)

    coins = users[user_id]["coins"]

    markup = types.InlineKeyboardMarkup(row_width=1)

    plans_btn = types.InlineKeyboardButton(
        "💰 تعرفه ها",
        callback_data="plans"
    )

    invite_btn = types.InlineKeyboardButton(
        "👥 دعوت دوستان",
        callback_data="invite"
    )

    support_btn = types.InlineKeyboardButton(
        "🛒 خرید و پشتیبانی",
        url="https://t.me/gost_support37"
    )

    markup.add(plans_btn, invite_btn, support_btn)

    bot.send_message(
        message.chat.id,
        f"""
🎉 به ربات Gost VPN خوش آمدید

🪙 تعداد سکه های شما: {coins}

👥 هر دعوت = 1 سکه
""",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    user_id = str(call.from_user.id)

    if call.data == "plans":

        bot.send_message(
            call.message.chat.id,
            """
💰 تعرفه ها:

1GB ➜ 50T
5GB ➜ 150T
10GB ➜ 250T

🛒 برای خرید روی دکمه خرید و پشتیبانی کلیک کنید.
"""
        )

    elif call.data == "invite":

        invite_link = f"https://t.me/{bot.get_me().username}?start={user_id}"

        bot.send_message(
            call.message.chat.id,
            f"""
👥 لینک دعوت شما:

{invite_link}

🪙 با هر دعوت 1 سکه دریافت میکنید.
"""
        )

bot.infinity_polling()
