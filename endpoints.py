import random

challenges = '/challenges'
todos = '/todos'
invalid_todo_endpoint = '/todo'
todo_id = f'/todos/{random.randint(1,10)}'
invalid_todo_id = f'/todos/{random.randint(999,9999)}'
challenger = '/challenger/'
done_status = '?doneStatus=true'
challenger_database = '/challenger/database/'
heartbeat = '/heartbeat'
secret_token = '/secret/token'
secret_note = '/secret/note'

