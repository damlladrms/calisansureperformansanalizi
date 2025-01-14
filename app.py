from flask import Flask, render_template, request, url_for, send_from_directory, abort
import os

app = Flask(__name__)

# Video yükleme klasörü
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# İzin verilen video formatları
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

# Upload klasörünü oluştur
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return 'Dosya seçilmedi', 400
    
    file = request.files['video']
    if file.filename == '':
        return 'Dosya seçilmedi', 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return {'success': True, 'filename': filename}
    
    return 'Geçersiz dosya formatı', 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)