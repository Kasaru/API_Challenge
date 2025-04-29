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