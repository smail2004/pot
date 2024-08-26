import telebot
from telebot import types
from time import sleep
admin =ضع ال الايدي هنا   
bot = telebot.TeleBot("ضع التكون هنا")
@bot.message_handler(commands=["start"])
def ss(message):
	bot.reply_to(message,"اهلًا بك في بوت التواصل ارسل رسالتك ")
@bot.message_handler(func=lambda message:True)
def ssss(message):
	if int(message.from_user.id) != admin:
		bot.forward_message(admin,message.chat.id ,message.message_id)
		sleep(1)
		bot.reply_to(message ,"تم ارسال رسالتك سيقوم مالك البوت بالرد عليك باقرب وقت")
	elif message.reply_to_message.forward_from and int(message.from_user.id) == admin:
		id = message.reply_to_message.forward_from.id
		bot.send_message(id,message.text)
		sleep(1)
		bot.reply_to(message ,"تم ارسال رسالتك للشخص")
bot.infinity_polling()