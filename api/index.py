from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import os
import sys
import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        logger.debug('Upload 요청 받음')
        logger.debug(f'Files in request: {request.files}')
        
        if 'file' not in request.files:
            logger.error('파일이 요청에 없음')
            return jsonify({'error': '파일이 없습니다'}), 400
        
        file = request.files['file']
        logger.debug(f'파일 이름: {file.filename}')
        
        result = cloudinary.uploader.upload(file)
        logger.debug(f'Cloudinary 응답: {result}')
        
        return jsonify({
            'success': True,
            'url': result['secure_url']
        })
    except Exception as e:
        logger.error(f'오류 발생: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 