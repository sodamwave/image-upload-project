from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import os
import traceback

app = Flask(__name__, static_folder='public')
CORS(app)

# Cloudinary 설정
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '파일이 없습니다'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '선택된 파일이 없습니다'}), 400
        
        # Cloudinary 업로드
        result = cloudinary.uploader.upload(file)
        return jsonify({
            'success': True,
            'url': result['secure_url']
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'details': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 