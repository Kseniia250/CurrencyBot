import telebot
import requests
import json

from config import API_KEY

keys = {
    'Рубль': 'RUB',
    'Евро': 'EUR',
    'Доллар': 'USD',
    'рубль': 'RUB',
    'евро': 'EUR',
    'доллар': 'USD',
    'руб': 'RUB',
    'Руб': 'RUB',
    'дол': 'USD',
    'Дол': 'USD',
    'долл': 'USD',
    'Долл': 'USD',
    'Рубли': 'RUB',
    'рубли': 'RUB'
}

class ConvertionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        # делаем запрос к API
        r = requests.get(f'https://api.currencyfreaks.com/latest?apikey={API_KEY}&symbols={quote_ticker},{base_ticker}')
        data = json.loads(r.content)
        rate_quote = float(data['rates'][quote_ticker])
        rate_base = float(data['rates'][base_ticker])

        # переводим из quote в base
        converted_amount = (rate_base / rate_quote) * amount

        return round(converted_amount, 2)
