from datetime import datetime
from drivers import sql_lite_driver as driver

def create(name, user_id):
    query = '''
        insert into quiz (user_id, name, create_date) values (?,?,?)
    '''
    now = datetime.now()
    row = (user_id, name, now.strftime(r"%d%m%Y"))
    id = driver.insert(query, row)
    print(f'Квиз создан под номером {id}')
    return id;

def get(quiz_id):
    query = '''
        select id, name from quiz where id = ?
    '''
    row = (quiz_id, )
    return driver.select(query, row)