from drivers import sql_lite_driver as driver

def create(name, quiz_id):
    questions = get_questions(quiz_id)
    num = len(questions)
    if num > 0:
        num = num + 1
    else:
        num = 1
    query = '''
        insert into question (quiz_id, name, num) values (?, ?, ?)
    '''
    row = (quiz_id, name, num)
    id = driver.insert(query, row)
    print(f'Вопрос создан под номером {id}')
    return id;

def get_questions(quiz_id):
    query = '''
        select id, name from question where quiz_id = ?
    '''
    row = (quiz_id, )
    return driver.select(query, row)

def get_question_by_id(id):
    query = '''
        select id, name, quiz_id from question where id = ?
    '''
    row = (id, )
    return driver.select(query, row)

def get_questions_by_num(quiz_id, num):
    query = '''
        select id, name from question where quiz_id = ? and num = ?
    '''
    row = (quiz_id, num, )
    return driver.select(query, row)