from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Cloudinary 설정 확인 및 초기화
try:
    cloudinary.config(
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key = os.environ.get('CLOUDINARY_API_KEY'),
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    )
except Exception as e:
    print(f"Cloudinary 설정 오류: {str(e)}")

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다'}), 400
    
    try:
        # 파일 이름 보안 처리
        filename = secure_filename(file.filename)
        
        # Cloudinary에 파일 업로드
        upload_result = cloudinary.uploader.upload(file)
        
        return jsonify({
            'message': '파일이 성공적으로 업로드되었습니다',
            'url': upload_result['secure_url']
        }), 200
        
    except Exception as e:
        print(f"업로드 오류: {str(e)}")
        return jsonify({'error': '파일 업로드 중 오류가 발생했습니다'}), 500

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 