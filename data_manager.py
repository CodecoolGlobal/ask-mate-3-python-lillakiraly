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
        WHERE question_id = %(id)s
        ORDER BY is_accepted DESC
        """
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
def add_new_question(cursor, user_id, question):
    query = """
        INSERT INTO question(submission_time, view_number, vote_number, title, message, image, user_id)
        VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, %(image)s, %(user_id)s)"""
    question['user_id'] = user_id
    value = question
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def add_new_answer(cursor, user_id, submission_time, question_id, message, image):
    query = """
        INSERT INTO answer(user_id, submission_time, vote_number, question_id, message, image)
        VALUES (%(user_id)s, %(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s)"""
    value = {
        'user_id': user_id,
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


# DELETE [target table]
# FROM    [table1]
#         INNER JOIN [table2]
# ON [table1.[joining column] = [table2].[joining column]
# WHERE   [condition]


# @database_common.connection_handler
# def delete_question_with_dependencies(cursor, question_id):
#     query = """
#         DELETE FROM question
#         JOIN answer ON answer.question_id = %(question_id)s
#         JOIN comment ON comment.answer_id = answer.id and comment.question_id = answer.question_id
#         WHERE question.id = %(question_id)s
#         AND answer.question_id = %(question_id)s
#         AND comment.answer_id = answer.id and comment.question_id = answer.question_id
#         """
#     cursor.execute(query, {'question_id': question_id})
#     return None


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


@database_common.connection_handler
def display_comment_from_question_id(cursor, question_id):
    query = """
        SELECT submission_time, message
        FROM comment
        WHERE question_id = %(question_id)s"""
    value = {'question_id': question_id}
    cursor.execute(query, value)
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
def display_comment_from_answer_id(cursor, answer_id):
    query = """
        SELECT submission_time, message
        FROM comment
        WHERE answer_id = %(answer_id)s"""
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_comment_to_question(cursor, comment):
    query = """
        INSERT INTO comment(user_id, question_id, message, submission_time, edited_count)
        VALUES (%(user_id)s, %(question_id)s, %(message)s, %(submission_time)s, 0)"""
    value = comment
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def add_new_comment_to_answer(cursor, user_id, answer_id, message, submission_time):
    query = """
        INSERT INTO comment(user_id, answer_id, message, submission_time, edited_count)
        VALUES (%(user_id)s ,%(answer_id)s, %(message)s, %(submission_time)s, 0)"""
    value = {
        'user_id': user_id,
        'answer_id': answer_id,
        'message': message,
        'submission_time': submission_time
    }
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def get_all_question_tags(cursor):
    query = """
        SELECT 
            DISTINCT ON (tag.name) name,
            tag.id
        FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_tags_by_question_id(cursor, question_id):
    query = """
        SELECT DISTINCT ON (tag.name) name, tag.id
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
def add_new_tag(cursor, new_tag):
    query = """
    INSERT INTO tag (name)
    VALUES (%(new_tag)s)
    """
    cursor.execute(query, {'new_tag': new_tag})
    return None


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
        SELECT
            answer.submission_time,
            answer.vote_number,
            answer.message,
            answer.image,
            comment.submission_time,
            comment.message,
            comment.edited_count
        FROM comment
        FULL JOIN answer ON answer.id = comment.answer_id
        INNER JOIN question ON question.id = answer.question_id
        WHERE answer.id = %(answer_id)s
    """
    value = {'answer_id': answer_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def does_user_exist(cursor, username):
    query = """
        SELECT CASE WHEN EXISTS (
            SELECT username
            FROM users
            WHERE username = %(username)s
        )
        THEN CAST(1 AS BIT)
        ELSE CAST(0 AS BIT) END"""
    value = {'username': username}
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def is_password_ok(cursor, username, password):
    query = """
        SELECT CASE WHEN EXISTS (
            SELECT password
            FROM users
            WHERE username = %(username)s AND password = %(password)s
        )
        THEN CAST(1 AS BIT)
        ELSE CAST(0 AS BIT) END"""
    value = {'username': username, 'password': password}
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def get_user_password(cursor, username):
    query = """
        SELECT password from users
        WHERE username = %(username)s"""
    value = {'username': username}
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def add_user_details(cursor, username, password, user_role='user'):
    query = """
        INSERT INTO users(username, password, user_role)
        VALUES (%(username)s, %(password)s, %(user_role)s)"""
    value = {'username': username, 'password': password, 'user_role': user_role}
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def get_user_id_from_username(cursor, username: str):
    query = """
        SELECT id
        FROM users
        WHERE username = %(username)s"""
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


@database_common.connection_handler
def check_if_question_author(cursor, question_id, user_id):
    query = """
        SELECT COUNT(question.id) AS is_author
        FROM question
        INNER JOIN users
        ON question.user_id = users.id
        WHERE users.id = %(user_id)s
        AND question.id = %(question_id)s
    """
    value = {'user_id': user_id, 'question_id': question_id}
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def get_if_theres_accepted_answer_to_question(cursor, question_id):
    query = """
        SELECT COUNT(*) AS is_accepted
        FROM answer
        WHERE is_accepted is TRUE
        AND question_id = %(question_id)s
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def set_answer_as_accepted(cursor, answer_id, is_accepted):
    query = """
        UPDATE answer
        SET is_accepted = %(is_accepted)s
        WHERE answer.id = %(answer_id)s
    """
    value = {'is_accepted': is_accepted,
              'answer_id': answer_id}
    cursor.execute(query, value)


@database_common.connection_handler
def get_users(cursor):
    query = """
        SELECT id, username, registration_date, reputation
        FROM users"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def change_reputation_value(cursor, user_id, increase_by):
    query = """
        UPDATE users
        SET reputation = reputation + %(increase_by)s
        WHERE id = %(user_id)s"""
    value = {
        'user_id': user_id,
        'increase_by': increase_by
    }
    cursor.execute(query, value)
    return None


@database_common.connection_handler
def get_user_id_from_question_or_answer_id(cursor, from_id, from_question_id=True):
    if from_question_id:
        query = """
            SELECT user_id
            FROM question
            WHERE id = %(from_id)s"""
    else:
        query = """
            SELECT user_id
            FROM answer
            WHERE id = %(from_id)s"""
    value = {'from_id': from_id}
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def get_tags_table(cursor):
    query = """
        SELECT DISTINCT ON(tag.name) name, COUNT(question_tag.tag_id)
        FROM tag
        INNER JOIN question_tag
        ON tag.id = question_tag.tag_id
        GROUP BY tag.id;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_from_user_id(cursor, user_id: int):
    query = """
        SELECT id, username, registration_date, reputation
        FROM users
        WHERE users.id = %(user_id)s"""
    value = {
        'user_id': user_id
    }
    cursor.execute(query, value)
    return cursor.fetchone()


@database_common.connection_handler
def get_num_of_data_from_user(cursor, user_id, table):
    query = sql.SQL("SELECT COUNT(*) AS num_of_data FROM {table} WHERE user_id = {user_id}").\
        format(table=sql.Identifier(table), user_id=sql.Literal(user_id))
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_question_ids_and_titles_from_user_id(cursor, user_id):
    query = """
        SELECT question.id, question.title
        FROM question
        WHERE user_id = %(user_id)s
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_ids_and_titles_with_corresponding_answers_from_user_id(cursor, user_id):
    query = """
        SELECT DISTINCT question.id, answer.message
        FROM question
        INNER JOIN answer
        ON answer.question_id = question.id
        WHERE answer.user_id = %(user_id)s;
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_ids_and_titles_with_corresponding_comments_from_user_id_question_id_given(cursor, user_id):
    query = """
        SELECT question.id, comment.message
        FROM comment
        INNER JOIN question
        ON comment.question_id = question.id
        WHERE comment.user_id = %(user_id)s;
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_ids_and_titles_with_corresponding_comments_from_user_id_answer_id_given(cursor, user_id):
    query = """
        SELECT question.id, comment.message
        FROM comment
        INNER JOIN answer
        ON comment.answer_id = answer.id
        INNER JOIN question
        ON answer.question_id = question.id
        WHERE comment.user_id = %(user_id)s;
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


