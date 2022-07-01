from psycopg2 import sql

import database_common


@database_common.connection_handler
def get_datas(cursor, table_name, col='id', is_ascending=True):
    order_ = 'ASC' if is_ascending else 'DESC'
    query = sql.SQL("select * from {table} ORDER BY {order_by} {order_}").\
        format(table=sql.Identifier(table_name), order_by=sql.Identifier(col), order_=sql.SQL(order_))
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def increase_view_number(cursor, id):
    query = """
            UPDATE question
            SET view_number = view_number + 1
            WHERE id = %(id)s"""
    value = {'id': id}
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def get_answers(cursor, id):
    query = """
        SELECT *
        FROM answer
        WHERE question_id = %(id)s"""
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    query = """
        SELECT *
        FROM answer
        WHERE id = %(answer_id)s"""
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def get_answer_id_by_question_id(cursor, question_id):
    query = """
        SELECT id
        FROM answer
        WHERE question_id = %(question_id)s"""
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def delete_question_tag_by_question_id(cursor, question_id):
    query = """
        DELETE FROM question_tag
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return None


@database_common.connection_handler
def delete_answers_by_question_id(cursor, question_id):
    query = """
        DELETE FROM answer
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return None


@database_common.connection_handler
def delete_question_by_question_id(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return None


@database_common.connection_handler
def delete_comment_by_question_id(cursor, question_id):
    query = """
        DELETE FROM comment
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return None


@database_common.connection_handler
def delete_comment_by_answer_id(cursor, answer_id):
    query = """
        DELETE FROM comment
        WHERE answer_id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return None


@database_common.connection_handler
def display_question_from_id(cursor, id):
    query = """
        SELECT *
        FROM question
        WHERE id = %(id)s"""
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def add_new_question(cursor, question):
    query = """
        INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
        VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, %(image)s)"""
    value = question
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def add_new_answer(cursor, submission_time, question_id, message, image):
    query = """
        INSERT INTO answer(submission_time, vote_number, question_id, message, image)
        VALUES (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s)"""
    value = {
        'submission_time': submission_time,
        'question_id': question_id,
        'message': message,
        'image': image
    }
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def vote_up_question(cursor, question_id):
    query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %(question_id)s"""
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def vote_down_question(cursor, question_id):
    query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %(question_id)s"""
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def vote_up_answer(cursor, answer_id):
    query = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %(answer_id)s"""
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def vote_down_answer(cursor, answer_id):
    query = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %(answer_id)s"""
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE id = %(answer_id)s"""
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
            DELETE FROM question
            WHERE id = %(question_id)s"""
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def edit_question(cursor, question_id, submission_time, title, message, image):
    query = """
        UPDATE question
        SET submission_time = %(submission_time)s, title = %(title)s, message = %(message)s, image = %(image)s
        WHERE id = %(question_id)s"""
    value = {
        'submission_time': submission_time,
        'title': title,
        'message': message,
        'question_id': question_id,
        'image': image
    }
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """
            DELETE FROM answer
            WHERE id = %(answer_id)s"""
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def edit_answer(cursor, new_answer):
    query = """
        UPDATE answer
        SET submission_time = %(submission_time)s, message = %(message)s, image = %(image)s
        WHERE id = %(id)s"""
    value = new_answer
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def get_search_results(cursor, search_phrase):
    query = """
        SELECT question.* FROM question
        LEFT JOIN answer ON answer.question_id = question.id 
        WHERE question.title ILIKE %(search_phrase)s OR question.message
        ILIKE %(search_phrase)s OR answer.message ILIKE %(search_phrase)s
        GROUP BY question.id
    """
    search_values = {'search_phrase': f'%{search_phrase}%'}
    cursor.execute(query, search_values)
    return cursor.fetchall()


# @database_common.connection_handler
# def get_search_results_from_answers(cursor, search_phrase):
#     query = """
#         SELECT message FROM answer
#         WHERE anmessage ILIKE %(search_phrase)s
#         GROUP BY
#     """
#     search_values = {'search_phrase': f'%{search_phrase}%'}
#     cursor.execute(query, search_values)
#     return cursor.fetchall()


@database_common.connection_handler
def display_comment_from_question_id(cursor, id):
    query = """
        SELECT submission_time, message
        FROM comment
        WHERE question_id = %(id)s"""
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def display_comment_from_answer_id(cursor, id):
    query = """
        SELECT submission_time, message
        FROM comment
        WHERE answer_id = %(id)s"""
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_comment_to_question(cursor, comment):
    query = """
        INSERT INTO comment(question_id, message, submission_time, edited_count)
        VALUES (%(question_id)s, %(message)s, %(submission_time)s, 0)"""
    value = comment
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def add_new_comment_to_answer(cursor, answer_id, message, submission_time):
    query = """
        INSERT INTO comment(answer_id, message, submission_time, edited_count)
        VALUES (%(answer_id)s, %(message)s, %(submission_time)s, 0)"""
    value = {
        'answer_id': answer_id,
        'message': message,
        'submission_time': submission_time
    }
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def get_all_question_tags(cursor):
    query = """
        SELECT tag.name, tag.id FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_tags_by_question_id(cursor, question_id):
    query = """
        SELECT tag.name, tag.id
        FROM tag
        JOIN question_tag
        ON question_tag.tag_id = tag.id
        WHERE question_tag.question_id = %(question_id)s;
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


def get_comment_by_id(cursor, comment_id):
    query = """
        SELECT *
        FROM comment
        WHERE id = %(comment_id)s"""
    value = {'comment_id': comment_id}
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def add_tags_to_question(cursor, question_id, tags):
    query = """
            INSERT INTO question_tag 
            VALUES (%(question_id)s, %(tag)s)
            """
    for tag in tags:
        cursor.execute(query, {'question_id': question_id, 'tag': tag})


@database_common.connection_handler
def add_new_tag(cursor, tag_id, new_tag):
    query = """
    INSERT INTO tag
    VALUES (%(tag_id)s, %(new_tag)s)
    """
    cursor.execute(query, {'tag_id': tag_id, 'new_tag': new_tag})


@database_common.connection_handler
def delete_tag_from_question(cursor, tag_id, question_id):
    query = """
        DELETE FROM question_tag
        WHERE question_id = %(question_id)s
        AND tag_id = %(tag_id)s
    """
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})


@database_common.connection_handler
def get_comments_by_answer_id(cursor, answer_id):
    query = """
        SELECT answer.submission_time, answer.vote_number, answer.message, answer.image, comment.submission_time, comment.message, comment.edited_count
        FROM comment
        FULL JOIN answer ON answer.id = comment.answer_id
        INNER JOIN question ON question.id = answer.question_id
        WHERE answer.id = %(answer_id)s
    """
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return cursor.fetchall()
