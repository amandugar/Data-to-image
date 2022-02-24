from flask import Flask, jsonify, send_file
import generate_images
from zipfile import ZipFile
import datetime
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Modern Algos Image Generator'

@app.route('/get_image', methods=['GET'])
def get_image():
    try:
        current_folder = os.path.dirname(os.path.abspath(__file__))
        for file in os.listdir(current_folder):
            if file.endswith(".zip") and file.startswith("images"):
                os.remove(file)
                
        for file in os.listdir(current_folder):
            if file.endswith(".jpg") and file.startswith("Image"):
                os.remove(file)
                
        image_names = generate_images.generate()
        image_name_1 = image_names[0]
        image_name_2 = image_names[1]
        today = str(datetime.date.today())
        random_number = str(datetime.datetime.now().microsecond)
        zip_file_name = 'images_' + today + '_' + random_number + '.zip'
        with ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(image_name_1)
            zip_file.write(image_name_2)
            
        return send_file(zip_file_name, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=False)