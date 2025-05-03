import random
import string
from faker import Faker

fake = Faker('ru_RU')

class DataGeneration:

    @staticmethod
    def generate_int():
        random_int = fake.random_int(min=1,max=100)
        return random_int

    @staticmethod
    def generate_wrong_id():
        random_id = fake.random_int(min=99999,max=999999)
        return  random_id

    @staticmethod
    def generate_long_text(length):
        all_symbols = string.ascii_uppercase + string.digits
        result = ''.join(random.choice(all_symbols) for _ in range(length))
        return result

    @staticmethod
    def generate_full_todo_body_json(title_length,doneStatus,description_length,with_space_at_the_end_of_title=False,with_space_at_the_end_of_description=False):
        if with_space_at_the_end_of_title:
            random_title = DataGeneration.generate_long_text(title_length) + ' '
            random_description = DataGeneration.generate_long_text(description_length)
            body = {
                'title': random_title,
                'doneStatus': doneStatus,
                'description': random_description
            }
        elif with_space_at_the_end_of_description:
            random_title = DataGeneration.generate_long_text(title_length)
            random_description = DataGeneration.generate_long_text(description_length) + ' '
            body = {
                'title': random_title,
                'doneStatus': doneStatus,
                'description': random_description
            }
        else:
            random_title = DataGeneration.generate_long_text(title_length)
            random_description = DataGeneration.generate_long_text(description_length)
            body = {
                'title': random_title,
                'doneStatus': doneStatus,
                'description': random_description
            }
        return body

    @staticmethod
    def generate_full_todo_body_xml(title_length, doneStatus,description_length):
        random_title = DataGeneration.generate_long_text(title_length)
        random_description = DataGeneration.generate_long_text(description_length)
        body = f'''
            <todo>
                <title>{random_title}</title>
                <doneStatus>{doneStatus}</doneStatus>
                <description>{random_description}</description>
            </todo>
            '''
        return body

    @staticmethod
    def generate_invalid_str_full_todo_body_json(title_length, doneStatus_length, description_length):
        random_title = DataGeneration.generate_long_text(title_length)
        random_description = DataGeneration.generate_long_text(description_length)
        random_status = DataGeneration.generate_long_text(doneStatus_length)
        body = {
            'title': random_title,
            'doneStatus': random_status,
            'description': random_description
        }
        return body

    @staticmethod
    def generate_invalid_str_full_todo_body_xml(title_length, description_length):
        random_title = DataGeneration.generate_long_text(title_length)
        random_description = DataGeneration.generate_long_text(description_length)
        body = f'''
                <todo>
                    <title>{random_title}</title>
                    <doneStatus>{random_title}</doneStatus>
                    <description>{random_description}</description>
                </todo>
                '''
        return body

    @staticmethod
    def generate_invalid_int_full_todo_body_json(title_length, description_length):
        random_title = DataGeneration.generate_long_text(title_length)
        random_description = DataGeneration.generate_long_text(description_length)
        random_status = DataGeneration.generate_int()
        body = {
            'title': random_title,
            'doneStatus': random_status,
            'description': random_description
        }
        return body

    @staticmethod
    def generate_invalid_int_full_todo_body_xml(title_length, description_length):
        random_title = DataGeneration.generate_long_text(title_length)
        random_description = DataGeneration.generate_long_text(description_length)
        random_status = DataGeneration.generate_int()
        body = f'''
                    <todo>
                        <title>{random_title}</title>
                        <doneStatus>{random_status}</doneStatus>
                        <description>{random_description}</description>
                    </todo>
                    '''
        return body

    @staticmethod
    def generate_unexpected_field_full_todo_body_json(title_length, doneStatus, description_length):
        random_title = DataGeneration.generate_long_text(title_length)
        random_description = DataGeneration.generate_long_text(description_length)
        body = {
            'title': random_title,
            'doneStatus': doneStatus,
            'description': random_description,
            'unrecognisedField' : 'unrecognisedField'
        }
        return body

    @staticmethod
    def generate_unexpected_field_full_todo_body_xml(title_length, doneStatus, description_length):
        random_title = DataGeneration.generate_long_text(title_length)
        random_description = DataGeneration.generate_long_text(description_length)
        body = f'''
                        <todo>
                            <title>{random_title}</title>
                            <doneStatus>{doneStatus}</doneStatus>
                            <description>{random_description}</description>
                            <unexpected_field>unexpected_field</unexpected_field>
                        </todo>
                        '''
        return body

    @staticmethod
    def generate_todo_body_without_title_json(doneStatus, description_length):
        random_description = DataGeneration.generate_long_text(description_length)
        body = {
            'doneStatus': doneStatus,
            'description': random_description
            }
        return body

    @staticmethod
    def generate_todo_body_without_title_xml(doneStatus, description_length):
        random_description = DataGeneration.generate_long_text(description_length)
        body = f'''
                <todo>
                    <doneStatus>{doneStatus}</doneStatus>
                    <description>{random_description}</description>
                </todo>
                '''
        return body

    @staticmethod
    def generate_todo_body_with_random_id_json(title_length, doneStatus, description_length, wrong_id=False):
        if wrong_id:
            random_id = DataGeneration.generate_wrong_id()
        else:
            random_id = DataGeneration.generate_int()
        random_title = DataGeneration.generate_long_text(title_length)
        random_description = DataGeneration.generate_long_text(description_length)
        body = {
            'id': random_id,
            'title': random_title,
            'doneStatus': doneStatus,
            'description': random_description
        }
        return body

    @staticmethod
    def generate_todo_body_with_random_id_xml(title_length,doneStatus,description_length):
        random_id = DataGeneration.generate_int()
        random_title = DataGeneration.generate_long_text(title_length)
        random_description = DataGeneration.generate_long_text(description_length)
        body = f"""
            <todo>
                    <id>{random_id}</id>
                    <title>{random_title}</title>
                    <doneStatus>{doneStatus}</doneStatus>
                    <description>{random_description}</description>
            </todo>
        """
        return body

    @staticmethod
    def generate_note_body():
        random_note = DataGeneration.generate_long_text(10)
        body = {
            'note' : random_note
        }
        return body

    @staticmethod
    def generate_one_field_todo_body_json(fieldname, value_length):
        random_value = DataGeneration.generate_long_text(value_length)
        body = {
            f'{fieldname}' : random_value
        }
        return body