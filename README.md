# Visual-Search

[![Generic badge](https://img.shields.io/badge/Python-3.6-blue.svg)](https://www.python.org/)
[![Generic badge](https://img.shields.io/badge/Framework-flask-green.svg)](https://flask.palletsprojects.com/en/1.1.x/)
[![Generic badge](https://img.shields.io/badge/Frontend-BootStrap-%238a2be2.svg)](https://getbootstrap.com/)
[![Generic badge](https://img.shields.io/badge/Database-Sqlite--3-yellowgreen.svg)](https://www.sqlite.org/index.html)

I created a Visual Search engine using Flask(Python) to find the similar products we want. It uses convolutional neural networks to extract feature maps of images which are present in the Database and recommend the similar products to the user based on the user's input using Nearest neighbors algorithm. 

## Watch Video Demo

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/53hdAGl2Zu4/0.jpg)](https://www.youtube.com/watch?v=53hdAGl2Zu4)

## How to run with your data?

* Create a new directory in data/dataset and place your data in that.
* Run the training.py to train the model on your data.
That's it. You are ready to find similarities by running run.py

## Creating your Environment

* Create a new Anaconda/Virtual Env in python.
* Install requirements by running the command - pip install requirements.txt
* Go to /app directory and run training.py
* Go to root folder and run run.py by using - python run.py
* Go to your browser and type http://127.0.0.1:5000/ in the address bar


## References 
* Frontend style - https://freefrontend.com/
* Scikit Learn - https://scikit-learn.org/
