from flask import Flask, render_template, request, redirect
import os
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MAX_IMAGE_SIZE = (1024, 1024)  # Adjust the maximum allowed image size as needed


def compress_image(input_path, output_path, quality=100):
    with Image.open(input_path) as img:
        img.thumbnail(MAX_IMAGE_SIZE)
        img.save(output_path, quality=quality)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files or 'name' not in request.form:
        return redirect(request.url)

    name = request.form['name']
    target_folder = os.path.join(app.config['UPLOAD_FOLDER'], name)

    # Create a folder with the user-entered name if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    files = request.files.getlist('files[]')

    for file in files:
        if file:
            filename = os.path.join(target_folder, file.filename)

            # Save the uploaded image temporarily
            file.save(filename)

            # Compress the image and overwrite the original
            compress_image(filename, filename)

    return 'Files uploaded and compressed successfully!'


if __name__ == '__main__':
    app.run(debug=True)
