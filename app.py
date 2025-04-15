from flask import Flask, request, jsonify
from core.data_processor import process_crime_data
from core.crime_model import CrimeAnalyzer
import os

app = Flask(__name__)

data_path = r"C:\Users\kspra\OneDrive\Desktop\CRIME ANALYSIS\data\newtrial - Sheet 1 - 01_District_wise_crim 2.csv"
print(f"Looking for dataset at: {os.path.abspath(data_path)}")
print(f"File exists: {os.path.exists(data_path)}")

df = process_crime_data(data_path)
if df is None:
    raise FileNotFoundError(f"Failed to load dataset at {data_path}. Verify the file exists and has the correct structure.")

try:
    analyzer = CrimeAnalyzer(df)
except Exception as e:
    raise RuntimeError(f"Failed to initialize CrimeAnalyzer: {str(e)}")

@app.route('/predict', methods=['POST'])
def predict_crime():
    try:
        input_data = request.get_json()
        if not input_data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        state = input_data.get('state')
        year = input_data.get('year')
        
        if not state or not year:
            return jsonify({'error': 'Missing state or year in request'}), 400
        
        year = int(year)
        
        prediction = analyzer.predict_crime_trend(state, year)
        return jsonify({'predicted_crime': prediction})
    except ValueError as ve:
        return jsonify({'error': f"Invalid input: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({'error': f"Prediction failed: {str(e)}"}), 500

# ✅ This is the key fix ↓↓↓
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
