from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
import re
import data_manager
from SETTINGS import PATH
from util import allowed_file, upload_image, modify_request_form

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = PATH


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
    return render_template("question_form.html", title=question_data['title'], question=question_data['message'], id=question_id, answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():    # sourcery skip: replace-interpolation-with-fstring, use-fstring-for-formatting
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
        return render_template('add_answer.html', id=question_id)
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
        return redirect("/list")
    return redirect("/list")


@app.route("/question/<int:question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    """ 8. Implement editing an existing question. """
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = request.form.get('title', '')
        message = request.form.get('message', '')

        data_manager.edit_question(question_id, submission_time, title, message)
        return redirect("/list")
    data = data_manager.display_question_from_id(question_id)
    return render_template("edit_question.html", data=data, id=question_id)


@app.route("/answer/<int:answer_id>/delete", methods=['GET'])
def delete_answer(answer_id):
    """ 9. Implement deleting an answer. """
    if request.method == 'GET':
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        data_manager.delete_answer(answer_id)
        return redirect(url_for('display_question', question_id=question_id['question_id']))
    return redirect("/list")


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
    for result in results:
        for key, text in result.items():
            if key != 'image':
                # result[key] = str(text).replace(search_phrase, '<span class="highlight">{}</span>'.format(search_phrase))
                result[key] = re.sub(search_phrase, f'<span class="highlight">{search_phrase}</span>', str(text), flags=re.IGNORECASE)
    return render_template('search.html', results=results)


@app.route('/question/<int:question_id>/new-comment')
def add_comment_to_question(question_id):
    return render_template('new_comment.html')


@app.route('/answer/<int:answer_id>/new-comment')
def add_comment_to_answer(answer_id):
    return render_template('new_comment.html')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8080
    )
