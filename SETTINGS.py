import os
from datetime import datetime

PATH = os.environ.get('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
SUBMISSION_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")