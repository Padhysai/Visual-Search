from app import app
from app import VisualSearch

from flask import render_template,request,redirect
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

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    items = []
    if request.method == "POST":

        if request.files:
            image = request.files["image"]
            image.save(app.config["IMAGE_UPLOAD_LOCATION"])
            #return redirect(request.url)

            search = VisualSearch.VisualSearch(dataset='example_dataset')
            search.run(app.config["IMAGE_UPLOAD_LOCATION"], model='Inception_Resnet', remove_not_white=False)
            items = search.similar_items_path()

    return render_template("public/recommend.html", items = items)