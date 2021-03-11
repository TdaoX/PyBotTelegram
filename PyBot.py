#Подключение библиотек
import telebot
import random
import sqlite3
from tkinter import *
from telebot import types

import config #подключение config содержащий токен бота для подключения его к телеграм
bot = telebot.TeleBot(config.TOKEN) #Подключение бота


@bot.message_handler(commands=['start']) #Команда start для начала работы с ботом
def welcome(message):


	
	sti = open('static/welcome.webp', 'rb') #Открытие файла со стикером
	bot.send_sticker(message.chat.id, sti) #Отправка стикера пользователю

	#Клавиатура бота
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Рандомное число")
	item2 = types.KeyboardButton("Как дела?")
	item3 = types.KeyboardButton("Бросить кубик")
	item4 = types.KeyboardButton("Порекомендуй музыку")
	item5 = types.KeyboardButton("Скинь картинку")
	
	markup.add(item1, item2, item3, item4, item5) #Подключение клавиатуры к боту
	
	idV2 = (message.from_user.id)
	db = sqlite3.connect('db2.db') #Подключение к базе данных (Пока что не реализовано )
	cursorObj = db.cursor() #Создание курсора для работы с базой данных
	cursorObj.execute("INSERT INTO users (user_id) VALUES(?)", (idV2,)) #Отправка данных в таблицу


	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup) #Отправка приветственного сообщения

@bot.message_handler(content_types=['text']) #Реализация работы клавиатуры бота
def lalala(message):
	if message.chat.type == 'private':
		if message.text == 'Рандомное число':
			bot.send_message(message.chat.id, str(random.randint(0,100)))
		
		elif message.text == 'Бросить кубик':
			bot.send_message(message.chat.id, str(random.randint(1,6)))

		elif message.text == 'Как дела?':
			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
			item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

			markup.add(item1, item2)
			bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)

		elif message.text == 'Порекомендуй музыку':
			markup = types.InlineKeyboardMarkup(row_width=3)
			item1 = types.InlineKeyboardButton("Rock", callback_data='rock')
			item2 = types.InlineKeyboardButton("Oppening", callback_data='oppening')
			item3 = types.InlineKeyboardButton("Jazz" , callback_data='jazz')


			markup.add(item1, item2, item3)
			bot.send_message(message.chat.id, 'Какой жанр предпочитаете?', reply_markup=markup)

		elif message.text == 'Скинь картинку':
			photo_number = random.randint(1,5)
			photo = open ('pictures/' + str(photo_number) + '.jpg', 'rb')
			bot.send_photo(message.chat.id, photo  );

		else:
			bot.send_message(message.chat.id, 'Я не знаю что ответить')

@bot.callback_query_handler(func=lambda call:True) #Реализация ответов на команды клавиатуры бота 

def callback_inline(call):
	try:
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		if call.message:
			if call.data == 'good':
				bot.send_message(call.message.chat.id, 'Вот и отлично')
			
			elif call.data == 'bad':
				bot.send_message(call.message.chat.id, 'Бывает')			
 			
			elif call.data == 'rock':
				music_rock_list = ['Кукла колдуна','Highway to Hell', 'Ночные ведьмы','Монстр','Атака мертвецов','Миллионник', 'Never Too Late', 'Thunder', 'Sweet Dreams', 'My Demons']
				music_rock = random.choice(music_rock_list)
				bot.send_audio(call.message.chat.id, open(r'music/rock/'+ music_rock +'.mp3', 'rb' ))
			
			elif call.data == 'oppening':
				music_oppening_list  = ['The Day','Iikara', 'Sore Wa Chiisana Hikari No Youna','Fire','veil','Clattanoia', 'Netsujo No Spectrum', 'From the Edge', 'Asphyxia', 'Lion']
				music_oppening = random.choice(music_oppening_list)
				bot.send_audio(call.message.chat.id, open(r'music/oppening/'+ music_oppening +'.mp3', 'rb' ))
			
			elif call.data == 'jazz':
				music_jazz_list  = ["Brenda Lee - Rockin' Around The Christmas Tree Single Version",'Michael Bublé - Holly Jolly Christmas', 
				'Ella Fitzgerald - Rudolph The Red-Nosed Reindeer','Nat King Cole - Jingle Bells','Валерий Сюткин - А снег идёт',
				'Michael Bublé - White Christmas', 'Ella Fitzgerald - Frosty the Snowman', 'Louis Armstrong - What A Wonderful World Single Version', 
				'Nat King Cole - L-O-V-E из сериала «Почему женщины убивают»', 'Michael Bublé - Mis Deseos _ Feliz Navidad (with Thalia)']
				music_jazz = random.choice(music_jazz_list)
				bot.send_audio(call.message.chat.id, open(r'music/jazz/'+ music_jazz +'.mp3', 'rb' ))
			
 			# show alert
			#bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				#text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")	

	except Exception as e:
		print(repr(e))

def start():
	#Запуск бота
	bot.polling(none_stop=True)



#интерфейс (сделан просто так)
root = Tk()
root.title("User Bot")
root.geometry("300x250")

Startbtn = Button(text="Запустить", command=start) #Кнопка запуска
Startbtn.pack()


root.mainloop()