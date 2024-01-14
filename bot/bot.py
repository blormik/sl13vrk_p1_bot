from pprint import pprint
import telebot
from telebot import types
import modules.quiz as quiz
import modules.question as question
import modules.answer as answer

BOT_LINK = 'https://t.me/sl13vrk_p1_bot'

bot = telebot.TeleBot('6493762259:AAHoVSit1pf3TNapKO75KWiHrpiPtb39FyU')

user_dict = {}        

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_dict[message.from_user.id] = {}    
    if len(message.text) > 6:
        quiz_id = message.text[7:]
        quiz_info = quiz.get(quiz_id)
        print(quiz_info)
        if quiz_info:
            text_message = f"Опрос на тему: {quiz_info[0][1]}"
            user_dict[message.from_user.id]['result'] = 0
            user_dict[message.from_user.id]['question_num'] = 1
            keyboard = types.InlineKeyboardMarkup()
            key = types.InlineKeyboardButton(text='Начать опрос', callback_data=f'start_quiz_' + str(quiz_info[0][0]))
            keyboard.add(key)
            bot.send_message(message.chat.id, text=text_message, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, text='Такого опроса не существует')
    else:
        text_message = "Это бот студента группы СЛ-13 Вильданова Р.К. и он поможет тебе сконструировать опрос:"
        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(text='Cоздать опрос', callback_data='new_quiz')
        keyboard.add(key)
        bot.send_message(message.chat.id, text=text_message, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'new_quiz':
        bot.send_message(call.message.chat.id, "Введите название опроса:")
        bot.register_next_step_handler(call.message, get_new_quiz_name)
    elif call.data == 'new_question':
        bot.send_message(call.message.chat.id, "Введите вопрос:")
        bot.register_next_step_handler(call.message, get_new_question_name)
    elif call.data == 'new_answer':
        bot.send_message(call.message.chat.id, "Введите ответ:")
        bot.register_next_step_handler(call.message, get_new_answer_name)
    elif call.data == 'quiz_done':
        print(user_dict[call.from_user.id]['quiz_id'])
        quiz_link = BOT_LINK + '?start=' + str(user_dict[call.from_user.id]['quiz_id'])
        text_message = f"Опрос завершен. Ссылка на опрос {quiz_link}"
        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(text='Cоздать опрос', callback_data='new_quiz')
        keyboard.add(key)
        bot.send_message(call.message.chat.id, text=text_message, reply_markup=keyboard)
    elif call.data == 'answer_done':
        text_message = 'Вопрос сохранен. Выберите правильный ответ'
        print(call.from_user.id)
        answers = answer.get_answers(user_dict[call.from_user.id]['question_id'])
        pprint(answers)
        keyboard = types.InlineKeyboardMarkup()
        for question_answer in answers:
            key = types.InlineKeyboardButton(text=question_answer[1], callback_data='answer_id_' + str(question_answer[0]))
            keyboard.add(key)
        bot.send_message(call.message.chat.id, text=text_message, reply_markup=keyboard)
    elif 'answer_id_' in call.data:
        answer_id = call.data[10:]
        print(answer_id)
        answer.set_right_answer(answer_id)
        text_message = 'Правильный ответ выбран.'
        keyboard = types.InlineKeyboardMarkup()
        add_quiz_key = types.InlineKeyboardButton(text='Cоздать вопрос', callback_data='new_question')
        quiz_done_key = types.InlineKeyboardButton(text='Завершить создание опроса', callback_data='quiz_done')       
        keyboard.add(add_quiz_key, quiz_done_key)
        bot.send_message(call.message.chat.id, text=text_message, reply_markup=keyboard)
    elif 'start_quiz_' in call.data:
        quiz_id = call.data[11:]
        register_answer(call, quiz_id)
    elif 'question_answer_result_id_' in call.data:
        answer_id = call.data[26:]
        user_id = call.from_user.id
        is_right = answer.is_right(answer_id)
        if is_right:
            user_dict[user_id]['result'] = user_dict[user_id]['result'] + 1
        current_answer = answer.get_answers_by_id(answer_id)
        print(current_answer)
        question_id = current_answer[0][2]
        quiz_info = question.get_question_by_id(question_id)
        quiz_id = quiz_info[0][2]
        pprint(quiz_id)
        register_answer(call, quiz_id)  

@bot.message_handler(content_types=['text'])
def callback_worker(message):
    if message.text == '/new_quiz': #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(message.from_user.id, "Введите название опроса")
        bot.register_next_step_handler(message, get_new_quiz_name)
    else:
        bot.send_message(message.chat.id, 'Не удалось создать опрос попробуй начать заного, набери /new_quiz');

def get_new_quiz_name(message):
    user_id = message.from_user.id
    quiz_id = quiz.create(message.text, user_id)
    user_dict[user_id]['quiz_id'] = quiz_id
    pprint(user_dict)
    text_message = "Опрос добавлен"
    keyboard = types.InlineKeyboardMarkup()
    add_quiz_key = types.InlineKeyboardButton(text='Cоздать вопрос', callback_data='new_question')
    quiz_done_key = types.InlineKeyboardButton(text='Завершить создание опроса', callback_data='quiz_done')
    keyboard.add(add_quiz_key, quiz_done_key)
    bot.send_message(user_id, text=text_message, reply_markup=keyboard)

def get_new_question_name(message):
    user_id = message.from_user.id
    question_id = question.create(message.text, user_dict[user_id]['quiz_id'])
    user_dict[user_id]['question_id'] = question_id
    pprint(user_dict)
    text_message = "Вопрос добавлен"
    keyboard = types.InlineKeyboardMarkup()
    create_answer_key = types.InlineKeyboardButton(text='Cоздать ответ', callback_data='new_answer')
    keyboard.add(create_answer_key)
    bot.send_message(user_id, text=text_message, reply_markup=keyboard)

def get_new_answer_name(message):
    user_id = message.from_user.id
    answer_id = answer.create(message.text, user_dict[user_id]['question_id'])
    pprint(user_dict)
    text_message = "Ответ добавлен"
    keyboard = types.InlineKeyboardMarkup()
    create_answer_key = types.InlineKeyboardButton(text='Cоздать ответ', callback_data='new_answer')
    answer_done_key = types.InlineKeyboardButton(text='Завершить ввод ответов', callback_data='answer_done')
    keyboard.add(create_answer_key).add(answer_done_key)
    bot.send_message(user_id, text=text_message, reply_markup=keyboard)

def set_answer(message):
    #Получаем все ответы
    keyboard = types.InlineKeyboardMarkup()
    create_answer_key = types.InlineKeyboardButton(text='Cоздать ответ', callback_data='new_answer')
    answer_done_key = types.InlineKeyboardButton(text='Завершить ввод ответов', callback_data='answer_done')
    keyboard.add(create_answer_key).add(answer_done_key)
    bot.send_message(message.from_user.id, reply_markup=keyboard)

def register_answer(call, quiz_id):
    user_id = call.from_user.id
    print(quiz_id)
    quiz_question = question.get_questions_by_num(quiz_id, user_dict[user_id]['question_num'])
    pprint(quiz_question)
    keyboard = types.InlineKeyboardMarkup()
    if quiz_question:
        answers = answer.get_answers(quiz_question[0][0])
        text_message = quiz_question[0][1]
        for question_answer in answers:
            key = types.InlineKeyboardButton(text=question_answer[1], callback_data='question_answer_result_id_' + str(question_answer[0]))
            keyboard.add(key)
        bot.send_message(call.message.chat.id, text=text_message, reply_markup=keyboard)          
        user_dict[user_id]['question_num'] = user_dict[user_id]['question_num'] + 1                
    else:
        quiz_question_all = question.get_questions(quiz_id)
        text_message = 'Результаты опроса: ' + str(user_dict[user_id]['result']) + ' из ' + str(len(quiz_question_all))
        bot.send_message(call.message.chat.id, text=text_message, reply_markup=keyboard)

def start_bot():
    bot.polling(none_stop=True, interval=0)