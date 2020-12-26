from app import app
from app import VisualSearch
import time

from flask import render_template,request,redirect,send_from_directory
from werkzeug.utils import secure_filename

@app.route("/")
def index():
    return render_template('public/index.html')

@app.route("/about")
def about():
    return render_template('public/about.html')

@app.route("/contact")
def contact():
    return render_template('public/contact.html')

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("my_dataset", filename)

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    items = []
    if request.method == "POST":

        if request.files:
            image = request.files["image"]
            image.save(app.config["IMAGE_UPLOAD_LOCATION"])
            #return redirect(request.url)
            start = time.process_time()
            search = VisualSearch.VisualSearch(dataset=app.config["DATASET"])
            search.run(app.config["IMAGE_UPLOAD_LOCATION"], model=app.config["MODEL_NAME"], remove_not_white=False)
            items = search.similar_items_path()
            print("Time taken : ", time.process_time() - start)

    return render_template("public/recommend.html", items = items)