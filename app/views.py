from app import app
from app import VisualSearch
import time
import json
import os

from flask import render_template,request,redirect,send_from_directory,make_response,jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

ProductsJSON = {}
@cross_origin()
@app.route("/")
def index():
    return render_template('public/index.html')

@cross_origin()
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(app.config["FAVICON_PATH"], 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@cross_origin()
@app.route("/about")
def about():
    return render_template('public/about.html')

@cross_origin()
@app.route("/contact")
def contact():
    return render_template('public/contact.html')

@cross_origin()
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory(app.config["DATASET_IMAGES_PATH"], filename)

@cross_origin()
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    global ProductsJSON
    f = open(app.config["JSON_PATH"])
    ProductsJSON = json.load(f)
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

            # Extracting Products Data
            res = []
            for item in items[0:16]:
                itm_q = {}
                itm = item.split('.')
                itm_p = ProductsJSON[itm[0]]
                itm_q['title'] = item
                itm_q['desc'] = itm[0]
                try:
                    itm_q['rating'] = itm_p['rating']
                except:
                    itm_q['rating'] = 2
                itm_q['URL'] = itm_p['URL']
                res.append(itm_q)

    return render_template("public/recommend.html", items = res)

@cross_origin()
@app.route("/items", methods=["GET", "POST"])
def items():
    global ProductsJSON
    f = open(app.config["JSON_PATH"])
    ProductsJSON = json.load(f)
    if request.method == "POST":
        #img = request.get_json()
        img = request.form['img']
        img_name = img.split('.')[0]
        img_rating = ProductsJSON[img_name]['rating']
        #resp = make_response(jsonify({"message": "OK"}), 200)
        img_path = os.path.join(app.config["DATASET_IMAGES_PATH"], img)
        start = time.process_time()
        search = VisualSearch.VisualSearch(dataset=app.config["DATASET"])
        search.run(img_path, model=app.config["MODEL_NAME"], remove_not_white=False)
        items = search.similar_items_path()
        print("Time taken : ", time.process_time() - start)

        # Extracting Products Data
        res = []
        for item in items[1:]:
            itm_q = {}
            itm = item.split('.')
            itm_p = ProductsJSON[itm[0]]
            itm_q['title'] = item
            itm_q['desc'] = itm[0]
            try:
                itm_q['rating'] = itm_p['rating']
            except:
                itm_q['rating'] = 2
            itm_q['URL'] = itm_p['URL']
            res.append(itm_q)
        #if request.headers['Content-Type'] == 'application/json':
           #return resp

    #return make_response(render_template("public/items.html", items = res))
    return render_template("public/items.html", items = res, image = img, image_name = img_name, image_rating = img_rating)
