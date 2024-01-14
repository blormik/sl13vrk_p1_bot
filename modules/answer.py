from drivers import sql_lite_driver as driver

def create(name, question_id):
    query = '''
        insert into answer (question_id, name, is_right) values (?, ?, 0)
    '''
    row = (question_id, name)
    id = driver.insert(query, row)
    print(f'Ответ создан под номером {id}')
    return id;

def get_answers(question_id):
    query = '''
        select id, name from answer where question_id = ?
    '''
    row = (question_id, )
    return driver.select(query, row)

def set_right_answer(answer_id):
    query = '''
        update answer set is_right = 1 where id = ?
    '''
    row = (answer_id, )
    return driver.update(query, row)