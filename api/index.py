from flask import Flask, request, send_from_directory
import pyrebase
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# Firebase 설정
config = {
    "apiKey": "your-api-key",
    "authDomain": "your-auth-domain",
    "projectId": "your-project-id",
    "storageBucket": "your-storage-bucket",
    "messagingSenderId": "your-sender-id",
    "appId": "your-app-id",
    "databaseURL": ""
}

# Firebase 초기화
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return {'error': '파일이 없습니다'}, 400
    
    file = request.files['file']
    
    if file.filename == '':
        return {'error': '선택된 파일이 없습니다'}, 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        try:
            # 임시로 파일 저장
            temp_path = f"/tmp/{unique_filename}"
            file.save(temp_path)
            
            # Firebase Storage에 업로드
            storage.child(f"images/{unique_filename}").put(temp_path)
            
            # 임시 파일 삭제
            os.remove(temp_path)
            
            # 업로드된 파일의 URL 가져오기
            file_url = storage.child(f"images/{unique_filename}").get_url(None)
            
            return {
                'message': '파일이 성공적으로 업로드되었습니다',
                'url': file_url
            }, 200
        
        except Exception as e:
            return {'error': f'업로드 중 오류 발생: {str(e)}'}, 500
    
    return {'error': '허용되지 않는 파일 형식입니다'}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 