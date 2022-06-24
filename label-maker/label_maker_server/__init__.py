from flask import Flask, render_template
from os import listdir
from os.path import isfile, join, basename, split
import json

BASE_DIR = os.environ.get('LABEL_MAKER_BASE_DIR')


def getImage(image_path):
    # Check if image has tag information

    head, tail = split(image_path)

    # Open annotation's file
    fname = join(head, '.label_maker', 'annotations.json') 
    with open(fname) as json_file:
        data = json.load(json_file)

    return data[tail]


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def default():

        BASE_IMG_PATH = 'http://localhost/images'

        collections = [f for f in listdir(BASE_DIR)]

        default_collection = collections[0]

        collection_image_path = join(BASE_DIR, default_collection)
        image_names = [f for f in listdir(collection_image_path)
                       if isfile(join(collection_image_path, f))]

        image_names = image_names[:10]

        curImage = getImage(join(collection_image_path, image_names[0]))
        return render_template(
            'base.html',
            image_names=image_names,
            base_image_path=BASE_IMG_PATH,
            collections=collections,
            default_collection=default_collection)

    # apply the blueprints to the app
    from label_maker_server import api
    app.register_blueprint(api.bp)

    return app

# def main():
#     app = Flask(__name__)
#     app.run(port=8080)


# if __name__ == '__main__':
#     print("Starting up")
#     main()
