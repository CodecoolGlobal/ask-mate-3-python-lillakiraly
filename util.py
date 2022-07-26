import os
from datetime import datetime

from flask import request
from werkzeug.utils import secure_filename

from SETTINGS import ALLOWED_EXTENSIONS, PATH, SUBMISSION_TIME
import bcrypt


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def get_user_login_info():
    return request.form.get('email', ''), request.form.get('password', '')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_timestamp():
    return str(datetime.now().timestamp())


def upload_image(file):  # sourcery skip: replace-interpolation-with-fstring, use-fstring-for-formatting
    filename = secure_filename(file.filename)
    image = '{}-{}'.format(int(datetime.now().timestamp()), filename)
    file.save(os.path.join(PATH, image))
    image = 'images/%s' % image
    return image


def modify_request_form(dict_, filename):
    dict_['submission_time'] = SUBMISSION_TIME
    dict_['image'] = filename
    return dict_


def modify_request_form_for_comment(dict_, question_id):
    dict_['question_id'] = question_id
    dict_['submission_time'] = SUBMISSION_TIME
    return dict_


