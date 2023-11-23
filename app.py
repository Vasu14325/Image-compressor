from flask import Flask, render_template, request, send_file
from PIL import Image
import io
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No selected file')
    if 'compression_factor' not in request.form:
        return render_template('index.html', error='please provide compression factor and check image format')
    original_image = Image.open(file)
    compression_factor = int(request.form['compression_factor'])
    compressed_image = compress_image(original_image, compression_factor)
    output = io.BytesIO()
    compressed_image.save(output, format='JPEG')
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='compressed_image.jpg')
def compress_image(image, factor):
    factor = max(55, min(factor, 95))
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=factor)
    output.seek(0)
    return Image.open(output)

if __name__ == '__main__':
    app.run(debug=True)
