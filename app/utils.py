import random


def generate_random_ticket() -> dict:
    dict_of_tickets = {
        'username': 'John_Doe',
        'price': random.randint(100, 300),
        'orders': random.randint(100, 300),
        'available': random.randint(100, 300),
        'max_limit': random.randint(100, 300),
        'min_limit': random.randint(1, 100),
        'rate': random.randint(1, 100),
        'pay_methods': {},
        'currency': random.choice(['usd', 'eur']),
        'coin': random.choice(['usdt', 'btc', 'eth', 'usdc', 'doge']),
        'trade_type': random.choice(['buy', 'sell']),
        'link': 'https://#',
        'exchange_id': random.randint(1, 5),
    }
    return dict_of_tickets
