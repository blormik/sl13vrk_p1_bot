from drivers import sql_lite_driver as driver

def create(name, quiz_id):
    query = '''
        insert into question (quiz_id, name) values (?, ?)
    '''
    row = (quiz_id, name)
    id = driver.insert(query, row)
    print(f'Вопрос создан под номером {id}')
    return id;