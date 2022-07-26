# TODO
# from bonus_questions import SAMPLE_QUESTIONS
#
# @app.route("/bonus-questions")
# def main():
#     return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from werkzeug.utils import secure_filename

import os
import re
import data_manager
import util
from SETTINGS import PATH, SUBMISSION_TIME
from util import allowed_file, upload_image, modify_request_form

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = PATH
app.secret_key = os.environ.get('SECRET_KEY', 'dev')


@app.route("/")
@app.route("/list", methods=['GET', 'POST'])
def home_page():
    """ 1. Implement the /list page that displays all questions
    """
    datas = data_manager.get_datas('question')
    if request.method == 'GET' and request.args.get('order_by'):
        order_direction = request.args.get('order_direction') == 'asc'
        datas = data_manager.get_datas(
            'question', col=request.args.get('order_by'), is_ascending=order_direction)
        return render_template("index.html", datas=datas)
    return render_template("index.html", datas=datas)


@app.route("/question/<int:question_id>", methods=['GET', 'POST'])
def display_question(question_id: int):
    """ 2. Create the /question/<question_id> page that displays a question and the answers for it. """
    data_manager.increase_view_number(question_id)
    question_data = data_manager.display_question_from_id(question_id)
    answers = data_manager.get_answers(question_id)
    question_comments = data_manager.display_comment_from_question_id(question_id)
    answer_comments = []
    for answer in answers:
        answer_comments.append(data_manager.display_comment_from_answer_id(answer['id']))
    question_tags = data_manager.get_question_tags_by_question_id(question_id)
    return render_template(
        "question_form.html",
        question_id=question_id,
        submission_time=question_data['submission_time'],
        title=question_data['title'],
        message=question_data['message'],
        view=question_data['view_number'],
        vote=question_data['vote_number'],
        image=question_data['image'],
        answers=answers,
        question_comments=question_comments,
        answer_comments=answer_comments,
        question_tags=question_tags)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():  # sourcery skip: replace-interpolation-with-fstring, use-fstring-for-formatting
    """ 3. Implement a form that allows the user to add a question. """
    if request.method != 'POST':
        return render_template('add_question.html')

    image = 'images/%s' % request.files.get('image', '').filename
    file = request.files['image']
    if file and allowed_file(file.filename):
        image = upload_image(file)

    question = modify_request_form(request.form.to_dict(), image)
    data_manager.add_new_question(question)
    return redirect('/list')


@app.route("/question/<int:question_id>/new-answer", methods=['POST', 'GET'])
def add_answer(question_id):  # sourcery skip: replace-interpolation-with-fstring
    if request.method != 'POST':
        return render_template('add_answer.html',
                               title='Add answer',
                               question_id=question_id,
                               action=url_for('add_answer', question_id=question_id))

    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    question_id = question_id
    message = request.form.get('message' '')
    image = 'images/%s' % request.files.get('image', '').filename

    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    data_manager.add_new_answer(submission_time, question_id, message, image)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<int:question_id>/delete", methods=['GET'])
def delete_question(question_id):
    """ 6. Implement deleting a question. """
    if request.method == 'GET':
        data_manager.delete_question(question_id)
        # answer_ids = data_manager.get_answer_id_by_question_id(question_id)
        # for answer_id in answer_ids:
        #     data_manager.delete_comment_by_answer_id(answer_id['id'])
        # data_manager.delete_comment_by_question_id(question_id)
        # data_manager.delete_answers_by_question_id(question_id)
        # data_manager.delete_question_tag_by_question_id(question_id)
        # data_manager.delete_question_by_question_id(question_id)
        return redirect("/list")
    return redirect("/list")


@app.route("/question/<int:question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    """ 8. Implement editing an existing question. """
    if request.method == 'POST':
        submission_time = SUBMISSION_TIME
        title = request.form.get('title', '')
        message = request.form.get('message', '')
        if request.files.get('uploaded_image').filename == '':
            image = request.form.get('default_image')
        else:
            image = 'images/%s' % request.files.get('uploaded_image').filename
            file = request.files['uploaded_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data_manager.edit_question(question_id, submission_time, title, message, image)
        return redirect(url_for('display_question', question_id=question_id))
    data = data_manager.display_question_from_id(question_id)
    return render_template("edit.html",
                           action=url_for('edit_question', question_id=question_id),
                           title='Edit question',
                           question_id=question_id,
                           question_to_update=data)


@app.route("/answer/<int:answer_id>/delete", methods=['GET'])
def delete_answer(answer_id):
    """ 9. Implement deleting an answer. """
    if request.method == 'GET':
        data_manager.delete_comment_by_answer_id(answer_id)
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        data_manager.delete_answer(answer_id)

        return redirect(url_for('display_question', question_id=question_id['question_id']))
    return redirect("/list")


# TODO
@app.route("/answer/<int:answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_answer_id(answer_id)
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    if request.method == 'POST':
        edited_answer = {
            'id': answer.get('id'),
            'submission_time': SUBMISSION_TIME,
            'question_id': answer.get('question_id'),
            'message': request.form.get('message', ''),
        }
        if request.files.get('uploaded_image').filename == '':
            edited_answer['image'] = request.form.get('default_image')
        else:
            edited_answer['image'] = 'images/%s' % request.files.get('uploaded_image').filename
            file = request.files['uploaded_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data_manager.edit_answer(edited_answer)
        return redirect(url_for('display_question', question_id=question_id['question_id']))

    return render_template("edit.html",
                           title='Edit answer',
                           question_id=question_id['question_id'],
                           answer_id=answer_id,
                           answer_to_update=answer)


# @app.route("/comment/<int:comment_id>/edit", methods=['GET', 'POST'])
# def edit_comment(comment_id):
#     answer = data_manager.get_comment_by_id(comment_id)
#     question_id = data_manager.get_question_id_by_answer_id(answer_id)
#     if request.method == 'POST':
#         edited_answer = {
#             'id': answer.get('id'),
#             'submission_time': SUBMISSION_TIME,
#             'question_id': answer.get('question_id'),
#             'message': request.form.get('message', ''),
#         }
#         data_manager.edit_answer(edited_answer)
#         return redirect(url_for('display_question', question_id=question_id['question_id']))
#
#     return render_template("edit.html",
#                            title='Edit answer',
#                            question_id=question_id['question_id'],
#                            answer_id=answer_id,
#                            answer_to_update=answer)


@app.route('/question/<int:question_id>/vote_up')
def vote_up_question(question_id):
    data_manager.vote_up_question(question_id)
    return redirect('/list')


@app.route('/question/<int:question_id>/vote_down')
def vote_down_question(question_id):
    data_manager.vote_down_question(question_id)
    return redirect('/list')


@app.route('/answer/<int:answer_id>/vote-up')
def vote_up_answer(answer_id):
    data_manager.vote_up_answer(answer_id)
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    return redirect(url_for('display_question', question_id=question_id['question_id']))


@app.route('/answer/<int:answer_id>/vote-down')
def vote_down_answer(answer_id):
    data_manager.vote_down_answer(answer_id)
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    return redirect(url_for('display_question', question_id=question_id['question_id']))


@app.route('/search')
def search_question():
    search_phrase = request.args.get('q')
    results = data_manager.get_search_results(search_phrase)
    highlight_prefix = '<span class="highlight">'
    highlight_suffix = '</span>'
    for result in results:
        for key, text in result.items():
            if key != 'image':
                # result[key] = str(text).replace(search_phrase, '<span class="highlight">{}</span>'.format(search_phrase))
                # result[key] = re.sub(search_phrase, f'<span class="highlight">{search_phrase}</span>', str(text),
                #                      flags=re.IGNORECASE)
                if locations := [i.span() for i in re.finditer(f'{search_phrase}', str(result[key]), flags=re.IGNORECASE)]:
                    for location in locations[::-1]:
                        result[key] = f'{str(result[key][:location[0]])}' \
                                      f'{highlight_prefix}{str(result[key])[location[0]:location[1]]}{highlight_suffix}' \
                                      f'{str(result[key])[location[1]:]}'

    return render_template('search.html', results=results)


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        message = util.modify_request_form_for_comment(request.form.to_dict(), question_id)
        data_manager.add_new_comment_to_question(message)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('new_comment_to_question.html', question_id=question_id)


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    if request.method == 'POST':
        message = request.form.get('message', '')
        data_manager.add_new_comment_to_answer(
            answer_id,
            message,
            SUBMISSION_TIME
        )
        return redirect(url_for('display_question', question_id=question_id['question_id']))
    return render_template('new_comment_to_answer.html', answer_id=answer_id, question_id=question_id['question_id'])


@app.route("/question/<int:question_id>/new-tag", methods=['GET', 'POST'])
def add_tag(question_id):
    all_tags = data_manager.get_all_question_tags()
    if request.method == 'POST' and request.form.get('new_tag', None):
        new_tag_added = request.form.get('new_tag', None)
        id_for_new_tag = max([tag['id'] for tag in all_tags]) + 1
        data_manager.add_new_tag(id_for_new_tag, new_tag_added)
        return redirect(url_for("add_tag", question_id=question_id))

    elif request.method == 'POST':
        add_tag_ids = []
        for tag in all_tags:
            is_valid_tag = request.form.get(tag['name'], None)
            if is_valid_tag:
                add_tag_ids.append(tag['id'])

        if add_tag_ids:
            data_manager.add_tags_to_question(question_id, add_tag_ids)
        return redirect(url_for('display_question', question_id=question_id))
# TODO fix UniqueViolation
    return render_template('add_tag.html', tags=all_tags, question_id=question_id)


@app.route('/question/<int:question_id>/tag/<int:tag_id>/delete')
def delete_question_tag(question_id, tag_id):
    data_manager.delete_tag_from_question(tag_id, question_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/authentication')
def authentication():
    return render_template('authentication.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    response_ok = make_response(render_template('login.html'), 200)
    response_forbidden = make_response(render_template('login.html'), 403)
    if request.method == 'POST':
        user_email, user_password = util.get_user_login_info()
        if data_manager.does_user_exist(user_email).get('case'):
            if util.verify_password(user_password, data_manager.get_user_password(user_email).get('password', '')):
                session['user'] = user_email
                session['answers'] = []
                return redirect('/')
            else:
                flash('Invalid password')
                return response_forbidden
        else:
            flash('Invalid username')
            return response_forbidden

    return response_ok

@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8080
    )
