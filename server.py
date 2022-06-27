from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

import os

import data_manager
import util

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/list", methods=['GET', 'POST'])
def home_page():
    """ 1. Implement the /list page that displays all questions """
    datas = data_manager.get_questions()
    # if request.method == 'GET':
    #     if request.args.get('order_by') == 'id':
    #         datas = data_handler.sort_questions(sorted_by='id', order=request.args.get('order_direction'))
    #     elif request.args.get('order_by') == 'submission_time':
    #         datas = data_handler.sort_questions(sorted_by='submission_time', order=request.args.get('order_direction'))
    #     elif request.args.get('order_by') == 'view_number':
    #         datas = data_handler.sort_questions(sorted_by='view_number', order=request.args.get('order_direction'))
    #     elif request.args.get('order_by') == 'vote_number':
    #         datas = data_handler.sort_questions(sorted_by='vote_number', order=request.args.get('order_direction'))
    #     elif request.args.get('order_by') == 'title':
    #         datas = data_handler.sort_questions(sorted_by='title', order=request.args.get('order_direction'),
    #                                             is_int_header=False)
    #     elif request.args.get('order_by') == 'message':
    #         datas = data_handler.sort_questions(sorted_by='message', order=request.args.get('order_direction'),
    #                                             is_int_header=False)
    #
    #     datas = util.convert_date(datas=datas)
    #     return render_template("index.html", datas=datas)
    # datas = util.convert_date(datas=datas)
    return render_template("index.html", datas=datas)


@app.route("/question/<int:question_id>")
def display_question(question_id: int):
    """ 2. Create the /question/<question_id> page that displays a question and the answers for it. """
    data_manager.increase_view_number(question_id)
    question_data = data_manager.display_question_from_id(question_id)
    answers = data_manager.get_answers(question_id)
    return render_template("question_form.html", title=question_data['title'], question=question_data['message'], id=question_id, answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    """ 3. Implement a form that allows the user to add a question. """
    questions = read_csv(reverse=False)
    if request.method == 'POST':
        added_question = {
            'id': util.generate_id(questions),
            'submission_time': util.convert_date(time_data=datetime.datetime.now()),
            'view_number': 0,
            'vote_number': 0,
            'title': request.form.get('title', ''),
            'message': request.form.get('message', ''),
            'image': 'images/%s' % request.files.get('image', '').filename
        }

        if 'image' not in request.files:
            flash('No file part')
            return redirect('/add-question')
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        export = append_line(questions, added_question)
        write_questions_to_csv(export)
        return redirect('/list')
    return render_template('add_question.html')


@app.route("/question/<int:question_id>/new-answer", methods=['POST', 'GET'])
def add_answer(question_id):
    answers = read_csv(csv_database='./sample_data/answer.csv', reverse=False)
    if request.method == 'POST':
        added_answer = {
            'id': util.generate_id(answers),
            'submission_time': util.convert_date(time_data=datetime.datetime.now()),
            'vote_number': 0,
            'question_id': question_id,
            'message': request.form.get('message' ''),
            'image': 'images/%s' % request.files.get('image', '').filename
        }

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        export = append_line(answers, added_answer)
        write_questions_to_csv(export, switch=False)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_answer.html', id=question_id)


def sorting_questions():
    """ 5. Implement sorting for the question list """
    pass


@app.route("/question/<int:question_id>/delete", methods=['GET'])
def delete_question(question_id):
    """ 6. Implement deleting a question. """
    if request.method == 'GET':
        data_handler.delete_line_by_id(question_id, "./sample_data/question.csv", QUESTION_HEADERS)
        return redirect("/list")
    return redirect("/list")


def upload_image():
    """ 7. Allow the user to upload an image for a question or answer. """
    pass


@app.route("/question/<int:question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    """ 8. Implement editing an existing question. """
    data = data_handler.read_csv()
    row = [item for item in data if int(item['id']) == question_id]
    if request.method == 'POST':
        edited_question = {
            "id": question_id,
            "submission_time": util.convert_date(time_data=datetime.datetime.now()),
            "view_number": request.form.get('view_number', ''),
            "vote_number": request.form.get('vote_number', ''),
            "title": request.form.get('title', ''),
            "message": request.form.get('message', ''),
            "image": 'images/'
        }

        file = request.files['uploaded_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if row[0]['image'] != f'images/{filename}':
                edited_question['image'] = f'images/{filename}'
        else:
            edited_question['image'] = row[0]['image']

        data_handler.edit_line_by_id(question_id, "./sample_data/question.csv", edited_question)
        return redirect("/list")
    return render_template("edit_question.html", data=row[0], id=question_id)


@app.route("/answer/<int:answer_id>/delete", methods=['GET'])
def delete_answer(answer_id):
    """ 9. Implement deleting an answer. """
    answers = read_csv("./sample_data/answer.csv")
    if request.method == 'GET':
        for answer in answers:
            if int(answer['id']) == answer_id:
                question_id = int(answer['question_id'])
                break
        data_handler.delete_line_by_id(answer_id, "./sample_data/answer.csv", data_handler.ANSWER_HEADERS)
        return redirect(url_for('display_question', question_id=question_id))
    return redirect("/list")


@app.route('/question/<int:question_id>/vote_up')
def vote_up_question(question_id):
    util.vote(question_id, 'sample_data/question.csv', 'up', switch=True)
    return redirect('/list')


@app.route('/question/<int:question_id>/vote_down')
def vote_down_question(question_id):
    util.vote(question_id, 'sample_data/question.csv', 'down', switch=True)
    return redirect('/list')


@app.route('/answer/<int:answer_id>/vote-up')
def vote_up_answer(answer_id):
    util.vote(answer_id, 'sample_data/answer.csv', 'up', switch=False)
    answers = read_csv('sample_data/answer.csv')
    for answer in answers:
        if int(answer['id']) == answer_id:
            break
    return redirect(url_for('display_question', question_id=answer['question_id']))


@app.route('/answer/<int:answer_id>/vote-down')
def vote_down_answer(answer_id):
    util.vote(answer_id, 'sample_data/answer.csv', 'down', switch=False)
    answers = read_csv('sample_data/answer.csv')
    for answer in answers:
        if int(answer['id']) == answer_id:
            break
    return redirect(url_for('display_question', question_id=answer['question_id']))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8080
    )
