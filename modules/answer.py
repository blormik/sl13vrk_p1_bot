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
        select id, name, question_id from answer where question_id = ?
    '''
    row = (question_id, )
    return driver.select(query, row)

def get_answers_by_id(id):
    query = '''
        select id, name, question_id from answer where id = ?
    '''
    row = (id, )
    return driver.select(query, row)

def set_right_answer(answer_id):
    query = '''
        update answer set is_right = 1 where id = ?
    '''
    row = (answer_id, )
    return driver.update(query, row)

def is_right(answer_id):
    query = '''
        select is_right from answer where is_right = 1 and id = ?
    '''
    row = (answer_id, )
    is_right_row = driver.select(query, row)
    if is_right_row:
        return True
    else:
        return False