from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_questions(cursor):
    query = """
        SELECT *
        FROM question"""
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
def display_question_from_id(cursor, id):
    query = """
        SELECT title, question.message
        FROM question
        WHERE id = %(id)s"""
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchall()
#
#
# @database_common.connection_handler
# def get_applicant_data_by_email_ending(cursor, email_ending):
#     pattern = f'%{email_ending}'
#     query = """
#         SELECT CONCAT(first_name, ' ', last_name) AS full_name, phone_number
#         FROM applicant
#         WHERE email LIKE %(email_ending)s"""
#     value = {'email_ending': pattern}
#     cursor.execute(query, value)
#     return cursor.fetchall()
#
#
# @database_common.connection_handler
# def get_applicant_data_by_name(cursor, first_name):
#     query = """
#         SELECT CONCAT(first_name, ' ', last_name) AS full_name, phone_number
#         FROM applicant
#         WHERE lower(first_name) = lower(%(first_name)s)"""
#     value = {'first_name': first_name}
#     cursor.execute(query, value)
#     return cursor.fetchall()
#
#
# @database_common.connection_handler
# def get_applicants(cursor):
#     query = """
#         SELECT CONCAT(first_name, ' ', last_name) AS full_name, phone_number, email, application_code
#         FROM applicant
#         ORDER BY first_name, last_name"""
#     cursor.execute(query)
#     return cursor.fetchall()
#
#
# @database_common.connection_handler
# def get_mentors(cursor):
#     query = """
#         SELECT CONCAT(first_name, ' ', last_name) AS full_name, city
#         FROM mentor
#         ORDER BY first_name"""
#     cursor.execute(query)
#     return cursor.fetchall()
#
#
# @database_common.connection_handler
# def get_mentors_by_last_name(cursor: RealDictCursor, last_name: str) -> list:
#     query = """
#         SELECT CONCAT(first_name, ' ', last_name) AS full_name, city
#         FROM mentor
#         WHERE lower(last_name) = lower(%(last_name)s)
#         ORDER BY first_name"""
#     value = {'last_name': last_name}
#     cursor.execute(query, value)
#     return cursor.fetchall()
#
#
# @database_common.connection_handler
# def get_city(cursor: RealDictCursor, city_name: str):
#     query = """
#         SELECT CONCAT(first_name, ' ', last_name) AS full_name, city
#         FROM mentor
#         WHERE lower(city) = lower(%(city_name)s)
#         ORDER BY first_name"""
#     value = {'city_name': city_name}
#     cursor.execute(query, value)
#     return cursor.fetchall()
#
#
# @database_common.connection_handler
# def edit_applicant_phone(cursor, phone_number, code):
#     query = """
#         UPDATE applicant
#         SET phone_number = %(phone_number)s
#         WHERE application_code = %(code)s"""
#     value = {'phone_number': phone_number,
#              'code': code}
#     cursor.execute(query, value)
#     return None
#
#
# @database_common.connection_handler
# def delete_applicant(cursor, code):
#     query = """
#         DELETE FROM applicant
#         WHERE application_code = %(code)s"""
#     value = {'code': code}
#     cursor.execute(query, value)
#     return None
#
#
# @database_common.connection_handler
# def delete_by_email(cursor, email_ending):
#     pattern = f'%{email_ending}'
#     query = """
#         DELETE FROM applicant
#         WHERE email LIKE %(email_ending)s"""
#     value = {'email_ending': pattern}
#     cursor.execute(query, value)
#     return None
#
#
# @database_common.connection_handler
# def add_applicant(cursor, first_name, last_name, phone_number, email, app_code):
#     query = """
#         INSERT INTO applicant (first_name, last_name, phone_number, email, application_code)
#         VALUES (%(first_name)s, %(last_name)s, %(phone_number)s, %(email)s, %(app_code)s)"""
#     values = {
#         'first_name': first_name,
#         'last_name': last_name,
#         'phone_number': phone_number,
#         'email': email,
#         'app_code': app_code,
#     }
#     cursor.execute(query, values)
#     return None
#
#
# @database_common.connection_handler
# def get_app_codes(cursor):
#     query = """
#         SELECT application_code
#         FROM applicant"""
#     cursor.execute(query)
#     return cursor.fetchall()
