import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# Use environment variables for safety
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")  # Include @ in value

bot = telebot.TeleBot(BOT_TOKEN)

bot.remove_webhook()

# Function to check if a user is a member of the channel
def is_user_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking user status: {e}")
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or 'User'

    if is_user_member(user_id):
        bot.reply_to(message, f"✅ Welcome, {username}! You are a member of {CHANNEL_USERNAME}.")
    else:
        join_link = f"https://t.me/{CHANNEL_USERNAME[1:]}"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔗 Join Channel", url=join_link))
        bot.reply_to(message, f"🚫 Hi {username}, please join {CHANNEL_USERNAME} to use this bot.", reply_markup=markup)

if __name__ == '__main__':
    print("🤖 Bot is running...")
    bot.infinity_polling()
