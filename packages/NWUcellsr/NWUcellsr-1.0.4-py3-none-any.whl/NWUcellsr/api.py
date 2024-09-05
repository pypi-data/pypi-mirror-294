from flask import Flask, request, jsonify
from super_resolution import process_image

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Super-Resolution API!"

@app.route('/super_resolution', methods=['POST'])
def super_resolution():
    img_file = request.files.get('image')
    if img_file is None:
        return jsonify({'status': 'error', 'message': 'No image file provided'}), 400

    try:
        # 处理图像
        output_image_path = process_image(img_file)
        return jsonify({'status': 'success', 'message': 'Image processed', 'output_image': output_image_path})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
