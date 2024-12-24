from flask import Flask, request, send_from_directory, jsonify
import cloudinary
import cloudinary.uploader
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Cloudinary 설정
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)


@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다'}), 400
    
    try:
        # Cloudinary에 파일 업로드
        result = cloudinary.uploader.upload(file)
        
        return jsonify({
            'message': '파일이 성공적으로 업로드되었습니다',
            'url': result['secure_url']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 