import telebot
import requests
import json
import random
from xml.etree import ElementTree

BOT_TOKEN = "1124923329:AAHDWe8MrTgApOPNp_6cUhOeL2dKmKew-MY"
MY_ID = 398782905
GROUP_CHAT_ID = -280569263
WEATHER_API = "62aff7c2ade4a091f1b127287c181fa0"

bot = telebot.TeleBot(BOT_TOKEN)

registered = []

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@bot.message_handler(commands=['currency'])
def weather_msg(message):
      try:
            response = requests.get('https://nationalbank.kz/rss/rates_all.xml')
            tree = ElementTree.fromstring(response.content)
            channel = tree.find('channel')
            rate_msg = "💸 Курс валют:"

            for item in channel.findall('item'):
                  name = item.find('title').text
                  if name == 'USD':
                        rate = item.find('description').text
                        change = item.find('change').text
                        rate_msg = rate_msg + ('\n💵 ' + name + ' ' + str(rate) + ' ' + str(change))
                  if name == 'EUR':
                        rate = item.find('description').text
                        change = item.find('change').text
                        rate_msg = rate_msg + ('\n💶 ' + name + ' ' + str(rate) + ' ' + str(change))
                        date = item.find('pubDate').text
                        rate_msg = rate_msg + ('\nАктуально на ' + str(date))

            bot.send_message(message.chat.id, rate_msg)
      except:
            bot.send_message(message.chat.id, "Ошибка со стороны серверов, сорян")

@bot.message_handler(commands=['weather'])
def weather_msg(message):
      try:
            raw_response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=almaty&lang=ru&units=metric&appid=' + WEATHER_API)
            weather = raw_response.json()

            weather_msg = "🌤 Погода в городе Алматы:\n"
            weather_msg = weather_msg + weather["weather"][0]["description"]
            weather_msg = weather_msg + "\n🌡 Температура: "
            weather_msg = weather_msg + str(weather["main"]["temp"]) + " °C"
            weather_msg = weather_msg + "\n🌡 Ощущается как: "
            weather_msg = weather_msg + str(weather["main"]["feels_like"]) + " °C"

            bot.send_message(message.chat.id, weather_msg)
      except:
            bot.send_message(message.chat.id, "Ошибка со стороны серверов, сорян")

@bot.message_handler(commands=['reg'])
def reg_msg(message):
      if message.from_user.first_name != None:      
            name = message.from_user.first_name
      else:
            name = ''

      if message.from_user.username != None:      
            username = "@" + message.from_user.username
      else:
            username = ''

      registered.append(name + " " + username)
      bot.send_message(message.chat.id, "Готово ебать")

@bot.message_handler(commands=['list'])
def list_msg(message):
      if len(registered) == 0:
            bot.send_message(message.chat.id, "Список пустой ало\n")      
            return

      response_msg = 'Список участников: \n'
      for user in registered:
            response_msg = response_msg + user + "\n"

      bot.send_message(message.chat.id, response_msg)

@bot.message_handler(commands=['pidor'])
def pidor_msg(message):
      if len(registered) == 0:
            bot.send_message(message.chat.id, "Список пустой ало\n")      
            return

      bot.send_message(message.chat.id, "Система поиска пидораса активирован!\n")
      bot.send_message(message.chat.id, "Пидор найден..\n")

      user_id = random.randrange(len(registered))
      bot.send_message(message.chat.id, "это " + registered[user_id])

@bot.message_handler(commands=['retard'])
def retard_msg(message):
      if len(registered) == 0:
            bot.send_message(message.chat.id, "Список пустой ало\n")      
            return

      bot.send_message(message.chat.id, "Ищем чорта в чате...\n")
      bot.send_message(message.chat.id, "Похоже он поступил как чорт\n")
      bot.send_message(message.chat.id, "и спрятался\n")
      bot.send_message(message.chat.id, "но я его нашел\n")
      bot.send_message(message.chat.id, "ъуъ сука\n")

      user_id = random.randrange(len(registered))
      bot.send_message(message.chat.id, "это " + registered[user_id])

@bot.message_handler(commands=['run'])
def retard_msg(message):
      if len(registered) == 0:
            bot.send_message(message.chat.id, "Список пустой ало\n")      
            return

      bot.send_message(message.chat.id, "Ищем красавчика в чате...\n")
      bot.send_message(message.chat.id, "Звоним Илону Маску\n")
      bot.send_message(message.chat.id, "запускаем FALCON\n")
      bot.send_message(message.chat.id, "FALCON падает...\n")
      bot.send_message(message.chat.id, "но мы успели найти красавчика\n")

      user_id = random.randrange(len(registered))
      bot.send_message(message.chat.id, "это " + registered[user_id])

@bot.message_handler(content_types=['text'])
def send_text(message):
      if message.from_user.id == MY_ID:
            if message.text.lower() == 'привет':
                  bot.send_message(message.chat.id, 'Привет, отец создатель')
            elif message.text.lower() == 'info':
                  bot.send_message(message.chat.id, message)
            elif message.text.lower() == 'пока':
                  bot.send_message(message.chat.id, 'Прощай, отец создатель')

bot.polling()