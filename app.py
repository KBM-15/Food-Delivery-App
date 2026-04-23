# app.py - Complete Food Delivery Data Analysis Application
# INF232 EC2 - Level 2 Computer Science Project

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.secret_key = 'food_delivery_secret_key_2024'

DATA_FILE = 'data/deliveries.csv'
os.makedirs('data', exist_ok=True)

# Initialize CSV with proper columns
if not os.path.exists(DATA_FILE):
    initial_df = pd.DataFrame(columns=[
        'timestamp', 'customer_age', 'customer_location', 'choose_meal',
        'order_value', 'delivery_time_min', 'delivery_fee', 'rating',
        'distance_km', 'weather_condition', 'time_of_day'
    ])
    initial_df.to_csv(DATA_FILE, index=False)
    print("✅ Created new data file")

# ==================== ROUTES ====================

@app.route('/')
def welcome():
    """Welcome/Home page"""
    return render_template('welcome.html')

@app.route('/order')
def order():
    """Order form page"""
    return render_template('order.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/analysis')
def analysis():
    """Advanced analysis page"""
    return render_template('analysis.html')

# ==================== API ENDPOINTS ====================

@app.route('/submit', methods=['POST'])
def submit():
    """Submit delivery data"""
    try:
        print("📨 Received submission")
        data = request.json
        print(f"Data received: {data}")
        
        # Add timestamp
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Convert to proper numeric types
        data['customer_age'] = int(data['customer_age'])
        data['order_value'] = float(data['order_value'])
        data['delivery_time_min'] = int(data['delivery_time_min'])
        data['delivery_fee'] = float(data['delivery_fee'])
        data['rating'] = int(data['rating'])
        data['distance_km'] = float(data['distance_km'])
        
        # Save to CSV
        df = pd.read_csv(DATA_FILE)
        new_row = pd.DataFrame([data])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        
        print(f"✅ Data saved! Total records: {len(df)}")
        
        return jsonify({
            'success': True,
            'message': 'Delivery data recorded successfully!',
            'data': data
        })
    except Exception as e:
        print(f"❌ Error in submit: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/descriptive_stats')
def descriptive_stats():
    """Get descriptive statistics"""
    try:
        print("📊 Fetching descriptive stats")
        
        # Check if file exists and has data
        if not os.path.exists(DATA_FILE):
            return jsonify({'total_responses': 0, 'message': 'No data file yet'})
        
        df = pd.read_csv(DATA_FILE)
        print(f"Dataframe shape: {df.shape}")
        
        if len(df) == 0:
            return jsonify({'total_responses': 0, 'message': 'No data yet'})
        
        # Convert columns to numeric where needed
        df['order_value'] = pd.to_numeric(df['order_value'], errors='coerce')
        df['delivery_time_min'] = pd.to_numeric(df['delivery_time_min'], errors='coerce')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['customer_age'] = pd.to_numeric(df['customer_age'], errors='coerce')
        df['delivery_fee'] = pd.to_numeric(df['delivery_fee'], errors='coerce')
        df['distance_km'] = pd.to_numeric(df['distance_km'], errors='coerce')
        
        stats = {
            'total_responses': len(df),
            'avg_order_value': round(df['order_value'].mean(), 2) if not df['order_value'].isna().all() else 0,
            'avg_delivery_time': round(df['delivery_time_min'].mean(), 1) if not df['delivery_time_min'].isna().all() else 0,
            'avg_rating': round(df['rating'].mean(), 2) if not df['rating'].isna().all() else 0,
            'avg_customer_age': round(df['customer_age'].mean(), 1) if not df['customer_age'].isna().all() else 0,
            'avg_delivery_fee': round(df['delivery_fee'].mean(), 2) if not df['delivery_fee'].isna().all() else 0,
            'avg_distance': round(df['distance_km'].mean(), 1) if not df['distance_km'].isna().all() else 0,
            'rating_distribution': {
                '5_star': int((df['rating'] == 5).sum()) if 'rating' in df else 0,
                '4_star': int((df['rating'] == 4).sum()) if 'rating' in df else 0,
                '3_star': int((df['rating'] == 3).sum()) if 'rating' in df else 0,
                '2_star': int((df['rating'] == 2).sum()) if 'rating' in df else 0,
                '1_star': int((df['rating'] == 1).sum()) if 'rating' in df else 0
            }
        }
        print(f"Stats calculated: {stats}")
        return jsonify(stats)
        
    except Exception as e:
        print(f"❌ Error in stats: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'total_responses': 0, 'error': str(e)}), 500

# Simple placeholder endpoints for advanced analysis
@app.route('/api/simple_regression')
def simple_regression():
    return jsonify({
        'technique': 'Simple Linear Regression',
        'description': 'Predicting delivery time based on distance',
        'message': 'Add more data to see regression results',
        'r2_score': 0,
        'equation': 'delivery_time = ? + ? × distance_km',
        'interpretation': 'Need at least 10 records for regression analysis'
    })

@app.route('/api/multiple_regression')
def multiple_regression():
    return jsonify({
        'technique': 'Multiple Linear Regression',
        'description': 'Analyzing multiple factors affecting delivery time',
        'message': 'Add more data to see regression results',
        'r2_score': 0,
        'interpretation': 'Need at least 15 records for multiple regression'
    })

@app.route('/api/pca')
def pca_analysis():
    return jsonify({
        'technique': 'Principal Component Analysis (PCA)',
        'description': 'Reducing data dimensions while preserving variance',
        'message': 'Add more data to see PCA results',
        'interpretation': 'Need at least 15 records for PCA analysis'
    })

@app.route('/api/classification')
def classification():
    return jsonify({
        'technique': 'Supervised Classification (Random Forest)',
        'description': 'Predicting fast vs slow deliveries',
        'message': 'Add more data to see classification results',
        'accuracy': 0,
        'interpretation': 'Need at least 20 records for classification'
    })

@app.route('/api/clustering')
def clustering():
    return jsonify({
        'technique': 'Unsupervised Classification (K-Means)',
        'description': 'Customer segmentation analysis',
        'message': 'Add more data to see clustering results',
        'interpretation': 'Need at least 15 records for clustering'
    })

if __name__ == '__main__':
    print("🚀 Starting FoodFlow Server...")
    print("📍 Access the application at: http://127.0.0.1:5000")
    print("📝 Available routes:")
    print("   - /          : Welcome page")
    print("   - /order     : Order form")
    print("   - /dashboard : Analytics dashboard")
    print("   - /analysis  : Advanced ML analysis")
    app.run(debug=True, host='0.0.0.0', port=5000)