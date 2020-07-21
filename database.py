from psycopg2 import connect, ProgrammingError
import psycopg2.errors
from contextlib import contextmanager
from local_settings import user, password, host, database
import datetime


@contextmanager
def database_operation():
    cnx = connect(user=user, password=password, host=host, database=database)
    c = cnx.cursor()
    yield c
    cnx.commit()
    c.close()
    cnx.close()


def create_main_table():
    try:
        with database_operation() as d:
            command_to_execute = '''
            CREATE TABLE words(id serial, en varchar(63), pl varchar(63), category smallint, created timestamp, 
            last_correct_answer timestamp);
            '''
            d.execute(command_to_execute)
    except psycopg2.errors.DuplicateTable:
        print('Table Duplicate')


def add_new_word(english, polish):
    try:
        with database_operation() as d:
            command_to_execute = '''
            INSERT INTO words(en, pl, category, created, last_correct_answer) VALUES ('{}', '{}', 0, now(), now())
            '''.format(english, polish)
            d.execute(command_to_execute)
    except Exception as e:
        print(e)


def change_category(last_correct_answer):
    current_date = datetime.datetime.now()
    if current_date > (last_correct_answer + datetime.timedelta(days=45)):
        return 6
    elif current_date > (last_correct_answer + datetime.timedelta(days=14)):
        return 5
    elif current_date > (last_correct_answer + datetime.timedelta(days=7)):
        return 4
    elif current_date > (last_correct_answer + datetime.timedelta(days=3)):
        return 3
    elif current_date > (last_correct_answer + datetime.timedelta(days=1)):
        return 2
    elif current_date > (last_correct_answer + datetime.timedelta(hours=6)):
        return 1
    return 0


def assign_categories():
    try:
        with database_operation() as d:
            command_to_execute = '''
            SELECT * FROM words;
            '''
            all_words = d.execute(command_to_execute)
            for word in d:
                print(word[0], word[1], '-', word[2], change_category(word[4]))
                with database_operation() as edit:
                    command_to_execute = '''
                    UPDATE words
                    SET category={}
                    WHERE id={}
                    '''.format(change_category(word[4]), word[0])
                    edit.execute(command_to_execute)
    except Exception as e:
        print(e)


def words_to_repeat():
    words_list = []
    current_date = datetime.datetime.now()
    try:
        with database_operation() as d:
            command_to_execute = '''
            SELECT * FROM words;
            '''
            all_words = d.execute(command_to_execute)
            for word in d:
                word_to_append = False
                category = word[3]
                last_correct_answer = word[5]
                if category == 0:
                    word_to_append = True
                elif category == 1:
                    if current_date > (last_correct_answer + datetime.timedelta(hours=6)):
                        word_to_append = True
                elif category == 2:
                    if current_date > (last_correct_answer + datetime.timedelta(days=1)):
                        word_to_append = True
                if word_to_append:
                    words_list.append((word[0], word[1], word[2]))

        return words_list

    except Exception as e:
        print(e)


def edit_record(column_name, word_id, new_value):
    with database_operation() as edit:
        command_to_execute = '''
        UPDATE words
        SET {}='{}'
        WHERE id={}
        '''.format(column_name, new_value, word_id)
        edit.execute(command_to_execute)


def category_action(word_id, action):
    current_time = datetime.datetime.now()
    category = None
    with database_operation() as d:
        command_to_execute = '''
        SELECT category FROM words WHERE id={} ;
        '''.format(word_id)
        d.execute(command_to_execute)
        for data in d:
            category = data[0]
            print(category)
        if action == '-':
            if category > 0:
                category -= 1
                print(category)
        elif action == '+':
            edit_record('last_correct_answer', word_id, current_time)
            if category < 7:
                category += 1
        edit_record('category', word_id, category)