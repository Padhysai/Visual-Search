import io
import numpy as np
import sqlite3
import tensorflow as tf
from tensorflow.python.keras.applications.vgg19 import preprocess_input as PP
from tensorflow.python.keras.preprocessing import image


import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


# adapters to store and retrieve numpy arrays in sqlite databases...
# https://www.pythonforthelab.com/blog/storing-data-with-sqlite/#storing-numpy-arrays-into-databases
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("array", convert_array)


class Training():

    def __init__(self, dataset):
        self.dataset = dataset
        self.features = []

    # method to calculate the features of every image and indicate in the database if the image is "active"
    def _calculate_features(self):
        """
        Calculates the feature map for given image.
        """

        def calculate_features(model, preprocessor, img):
            # preprocess the image
            img = image.img_to_array(img)  # convert to array

            img = np.expand_dims(img, axis=0)

            img = preprocessor(img)

            return model.predict(img).flatten()

        transformations = ['000']

        # load VGG model
        print("Loading VGG pre-trained model...")
        VGG_model = tf.keras.models.load_model('C:/Users/91955/Desktop/current/Visual-Search/data/models/model.h5')

        # connect to the database, and create the features table if it does not exists
        os.makedirs(parentdir + '\\data\\database', exist_ok=True)
        conn = sqlite3.connect(parentdir + '\\data\\database\\features.db', detect_types=sqlite3.PARSE_DECLTYPES)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS features_' + str(
            self.dataset) + ' (img_id TEXT PRIMARY KEY, item_id TEXT, features_VGG array, transformation CHARACTER(20), white_background INTEGER, active INTEGER)')

        # create a item ID: list of associated image IDs dictionary, useful to identify most similar items after computation
        folder = parentdir + '\\data\\dataset\\' + self.dataset

        # extract the id of the items and of the images in the dataset
        images = os.listdir(folder)
        items = [i.split('_')[0].split('.')[0] for i in images]
        self.item_to_img = {items[i]: [j for j in images if j.split('_')[0].split('.')[0] == items[i]] for i in
                            range(len(items))}  # dictionary item ID: img ID
        self.img_to_item = {i: i.split('_')[0].split('.')[0] for i in images}

        # loop through the images, to extract their features.
        cur.execute('UPDATE features_' + str(self.dataset) + ' SET active = ?', (0,))
        ki = 0
        for i in images:
            img_ids = [i + ',' + j for j in transformations]
            cur.execute('SELECT img_id, item_id FROM features_' + str(self.dataset) + ' WHERE img_id IN ({})'.format(
                ','.join('?' * len(transformations))),
                        img_ids)
            data = cur.fetchall()

            path = folder + '\\' + i
            img_VGG = image.load_img(path, target_size=(224, 224))

            for j in range(len(transformations)):
                # if already calculated, we activate it
                if img_ids[j] in [x[0] for x in data]:
                    cur.execute('UPDATE features_' + str(self.dataset) + ' SET active = ? WHERE img_id = ?',
                                (1, img_ids[j]))

                # otherwise, we calculate it
                else:
                    # VGG model
                    features_VGG = calculate_features(model=VGG_model, preprocessor=PP, img=img_VGG)

                    # Verify color of the background (if white or not)
                    if np.array(img_VGG)[0][0][0] == 255:
                        white_background = 1
                    else:
                        white_background = 0

                    cur.execute('INSERT INTO features_' + str(
                        self.dataset) + ' (img_id, item_id, features_VGG, transformation, white_background, active) VALUES (?,?,?,?,?,?)',
                                (img_ids[j], i.split('_')[0].split('.')[0], features_VGG, transformations[j],
                                 white_background, 1))

            ki += 1
            if ki % 100 == 1:
                # commit changes
                conn.commit()
                print('Features calculated for', ki, 'images')

        conn.commit()
        cur.close()
        conn.close()

    # main method to extract features
    def fit(self):

        # calculate the features
        self._calculate_features()
        print('Training Completed')


if __name__ == '__main__':
    train = Training(dataset='my_dataset')
    train.fit()