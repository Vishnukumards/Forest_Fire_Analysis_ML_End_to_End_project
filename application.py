import pickle
from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

# Load model and scaler
ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
standard_scaler = pickle.load(open('models/scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_data():
    if request.method == 'POST':
        try:
            # Extract form data
            data = [
                float(request.form.get('Temperature')),
                float(request.form.get('RH')),
                float(request.form.get('Ws')),
                float(request.form.get('Rain')),
                float(request.form.get('FFMC')),
                float(request.form.get('DMC')),
                float(request.form.get('ISI')),
                float(request.form.get('Classes')),
                float(request.form.get('Region'))
            ]

            # Scale and predict
            scaled_data = standard_scaler.transform([data])
            prediction = ridge_model.predict(scaled_data)[0]

            return render_template('index.html', result=round(prediction, 2))
        except Exception as e:
            return render_template('index.html', result=f"Error: {str(e)}")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
