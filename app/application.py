import os
import io
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from mosaic import find_mosaic_url
from postit import sync_board
from food import add_reminders
from router import classify_image

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(request_files):
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return 
    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    return file_path

@application.route('/', methods=['GET', 'POST'])
def router():
    if request.method == 'POST':
        file_path = upload_file(request.files)
        if not file_path:
            return redirect(request.url)

        classification = classify_image(img_path=file_path)
        if classification == 'food':
            menu_items = add_reminders(img_path=file_path)
            os.remove(file_path)
            return render_template('food_success.html', menu_items=menu_items)
        if classification == 'mosaic':
            url = find_mosaic_url(img_path=file_path)
            os.remove(file_path)
            return redirect(url)
        return render_template('route.html', classification=classification)
    return render_template('home.html')

@application.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
        file_path = upload_file(request.files)
        if not file_path:
            return redirect(request.url)
            
        menu_items = add_reminders(img_path=file_path)
        os.remove(file_path)
        return render_template('food_success.html', menu_items=menu_items)

    return render_template('food.html')

@application.route('/mosaic', methods=['GET', 'POST'])
def mosaic():
    if request.method == 'POST':
        file_path = upload_file(request.files)
        if not file_path:
            return redirect(request.url)
            
        url = find_mosaic_url(img_path=file_path)
        os.remove(file_path)
        return redirect(url)

    return render_template('mosaic.html')

@application.route('/postit', methods=['GET', 'POST'])
def postit():
    if request.method == 'POST':
        file_path = upload_file(request.files)
        if not file_path:
            return redirect(request.url)
            
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
application.secret_key = 'super secret key'

