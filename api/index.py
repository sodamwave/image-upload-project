from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import os
from datetime import datetime

app = Flask(__name__)

# Cloudinary 설정
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '파일이 없습니다.'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '선택된 파일이 없습니다.'}), 400

        # Cloudinary에 업로드
        result = cloudinary.uploader.upload(file)
        
        return jsonify({
            'url': result['secure_url'],
            'public_id': result['public_id']
        })

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': '업로드 중 오류가 발생했습니다.'}), 500

if __name__ == '__main__':
    app.run(debug=True) 