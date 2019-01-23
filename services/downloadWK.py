# author: tiankai
# copywrite 2019

import shutil
import os
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    url_for, flash, send_file, send_from_directory, make_response
)
from werkzeug.exceptions import abort

from services.auth import login_required
from services.utils import init_webdriver, download

bp = Blueprint('downloadWK', __name__, url_prefix='/downloadWK')

# ---------------------------------------------------------------
# driver initialization
# ---------------------------------------------------------------
driver = init_webdriver()

# ---------------------------------------------------------------
# route & view
# ---------------------------------------------------------------
@bp.route('/', methods=('GET', 'POST'))
def index():

    if request.method == 'POST':

        download(driver, request.form['fileURL'])
        # waiting for finishing download
        time.sleep(3)

        # root directory
        root_dir = 'services/static'
        files = os.listdir(os.path.join(root_dir, 'tmp'))

        shutil.move(os.path.join(root_dir, 'tmp', files[0]), os.path.join(root_dir, 'downloaded', files[0]))

        return redirect(url_for('downloadWK.file_download', filename=files[0]))

    return render_template('downloadWK/index.html')

@bp.route('/downloaded/<filename>', methods=('GET', ))
def file_download(filename):

    root_dir = 'static/downloaded'

    response = make_response(send_from_directory(root_dir, filename, as_attachment=True))

    # response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode('utf-8').decode('utf-8'))

    return response
