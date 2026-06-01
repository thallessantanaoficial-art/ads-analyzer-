from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from utils.analyzer import AdsAnalyzer
from werkzeug.utils import secure_filename
import io

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze the file
        analyzer = AdsAnalyzer(filepath)
        metrics = analyzer.calculate_metrics()
        insights = analyzer.generate_insights()
        daily_performance = analyzer.get_daily_performance()
        
        # Clean up - remove uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'insights': insights,
            'daily_performance': daily_performance[:30]  # Last 30 days
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sample-template')
def sample_template():
    """Download sample CSV template"""
    try:
        csv_content = """Date,Impressions,Clicks,Cost,Conversions,Conversion Value
2024-05-01,5000,250,75.50,10,500
2024-05-02,5200,280,84.00,12,600
2024-05-03,4800,240,72.00,9,450
2024-05-04,5500,300,90.00,14,700
2024-05-05,5100,265,79.50,11,550"""
        
        return send_file(
            io.BytesIO(csv_content.encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='ads-template.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
