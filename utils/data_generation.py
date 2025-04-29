import random
import string

from faker import Faker

fake = Faker('ru_RU')

class DataGeneration:
    @staticmethod
    def generate_name():
        random_name = fake.company()
        return random_name

    @staticmethod
    def generate_description():
        random_description = fake.text()
        return random_description

    @staticmethod
    def generate_word():
        random_word = fake.name()
        return random_word

    @staticmethod
    def generate_int():
        random_int = fake.random_int(min=1,max=100)
        return random_int

    @staticmethod
    def generate_long_text(length):
        all_symbols = string.ascii_uppercase + string.digits
        result = ''.join(random.choice(all_symbols) for _ in range(length))
        return result