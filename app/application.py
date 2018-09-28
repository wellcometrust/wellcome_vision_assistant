import os
import io
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from mosaic_utils import find_mosaic_url
from postit_utils import sync_board

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            url = find_mosaic_url(img_path=file_path)
            os.remove(file_path)
            return redirect(url)

    return render_template('mosaic.html')

@application.route('/postit', methods=['GET', 'POST'])
def postit_upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            closed_issues = sync_board(file_path)
            os.remove(file_path)
            return render_template('sync.html', closed_issues=",".join(["#"+str(iss) for iss in closed_issues]))

    return render_template('postit.html')

from werkzeug import SharedDataMiddleware
application.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
application.wsgi_app = SharedDataMiddleware(application.wsgi_app, {
    '/uploads':  application.config['UPLOAD_FOLDER']
})

