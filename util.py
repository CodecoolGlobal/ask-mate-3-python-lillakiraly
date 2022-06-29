import os
from datetime import datetime

from werkzeug.utils import secure_filename

from SETTINGS import ALLOWED_EXTENSIONS, PATH, SUBMISSION_TIME


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
