import os
import datetime
import uuid
from flask import Flask, request, jsonify, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r"C:\exselentim\python\file_pro\uploads"
app.config['OUTPUTS_FOLDER'] = r"C:\exselentim\python\file_pro\outputs"

"""
    This is a simple web app that allows users to upload files and get explanations for them.
"""
@app.route('/upload', methods=['POST'])
def upload() -> jsonify:
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    uid = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = secure_filename(file.filename)
    new_filename = f"{filename}_{timestamp}_{uid}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

    return jsonify({'uid': uid}), 200

"""
    This endpoint returns the status of a file.
"""
@app.route('/status/<uid>', methods=['GET'])
def status(uid) -> jsonify:
    matching_files = [file for file in os.listdir(app.config['UPLOAD_FOLDER']) if uid in file]
    if len(matching_files) == 0:
        return jsonify({'status': 'not found', 'filename': None, 'timestamp': None, 'explanation': None}), 404

    for filename in os.listdir(app.config['OUTPUTS_FOLDER']):
        if uid in filename:
            output_path = os.path.join(app.config['OUTPUTS_FOLDER'], filename)
            if os.path.exists(output_path):
                with open(output_path, 'r') as output_file:
                    explanation = json.load(output_file)
                original_filename, timestamp, _ = filename.split('_', 2)
                return jsonify({'status': 'done', 'filename': original_filename, 'timestamp': timestamp,
                                'explanation': explanation}), 200
    return jsonify({'status': 'pending', 'filename': None, 'timestamp': None, 'explanation': None}), 200


if __name__ == '_main_':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['OUTPUTS_FOLDER']):
        os.makedirs(app.config['OUTPUTS_FOLDER'])
    app.run()
