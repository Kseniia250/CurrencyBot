import telebot
from extensions import ConvertionException, CurrencyConverter, keys
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    bot.reply_to(message, f'Привет, {message.chat.username}!🌟\n'
                          f'Я - бот, который подскажет текущие курсы валют!💰\n'
                          f'Чтобы начать работу со мной, введите запрос в следующем формате:\n'
                          f'<имя валюты><в какую валюту перевести><сумма переводимой валюты>\n'
                          f'Например: рубль доллар 5000\n'
                          f'Чтобы увидеть список всех валют введите команду /values')

@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    limited_keys = list(keys.keys())[:3]  # берём только первые 3 ключа
    text = 'Доступные валюты:\n' + '\n'.join(limited_keys)
    bot.reply_to(message, text)

# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    bot.reply_to(message, "Вау! Очень красивое фото!")

@bot.message_handler(content_types=['voice', 'audio'])
def handle_docs_voice(message):
    bot.reply_to(message, "Звучит чудесно!")


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров! ')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)

    except ConvertionException as e:
        bot.send_message(message.chat.id, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать команду:\n{e}")
    else:
        text = f'Цена {amount} {quote} в {base} — {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)




