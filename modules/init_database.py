import drivers.sql_lite_driver as driver

tables = [
    [
        'quiz',
        ''' 
            CREATE TABLE IF NOT EXISTS quiz (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                name TEXT,
                create_date TEXT
            );
        '''
    ],
    [
        'question',
        '''
            CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                name TEXT
            );
        '''
    ],
    [
        'answer',
        '''
            CREATE TABLE IF NOT EXISTS answer (
                id INTEGER PRIMARY KEY,
                question_id INTEGER,
                name TEXT,
                is_right INTEGER
            );
        '''
    ]
]

def main():
    for table in tables:
        if not driver.is_table_exist(table[0]):
            driver.create_table(table[1])
