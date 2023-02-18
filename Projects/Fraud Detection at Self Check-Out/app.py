from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# Load the model and preprocessor
model = pickle.load(open('models/model.pkl','rb'))
scaler = pickle.load(open('models/scaler.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    # Get the data from the form
    totalScanTimeInSeconds = int(request.form.get("totalScanTimeInSeconds"))
    grandTotal = int(request.form.get("grandTotal"))
    lineItemVoids = int(request.form.get("lineItemVoids"))
    scansWithoutRegistration = int(request.form.get("scansWithoutRegistration"))
    quantityModifications = int(request.form.get("quantityModifications"))
    scannedLineItemsPerSecond = float(request.form.get("scannedLineItemsPerSecond"))
    valuePerSecond = float(request.form.get("valuePerSecond"))
    lineItemVoidsPerPosition = float(request.form.get("lineItemVoidsPerPosition"))
    Trust_level = str(request.form.get("Trust_level"))

    # Create a Pandas DataFrame with the input data
    data = pd.DataFrame({
        'totalScanTimeInSeconds': [totalScanTimeInSeconds],
        'grandTotal': [grandTotal],
        'lineItemVoids': [lineItemVoids],
        'scansWithoutRegistration': [scansWithoutRegistration],
        'quantityModifications': [quantityModifications],
        'scannedLineItemsPerSecond': [scannedLineItemsPerSecond],
        'valuePerSecond': [valuePerSecond],
        'lineItemVoidsPerPosition': [lineItemVoidsPerPosition],
        'Trust_level': [Trust_level]
    })

    # Select only the numeric columns
    numeric_columns = data.select_dtypes(include='number').columns
    numeric_data = data[numeric_columns]

    # Scale the numeric data using MinMaxScaler
    scaled_numeric_data = scaler.transform(numeric_data)
    scaled_numeric_df = pd.DataFrame(scaled_numeric_data, columns=numeric_columns)

    # Create dummy variables for the trustLevel column
    Trust_level_2 = 0
    Trust_level_3 = 0
    Trust_level_4 = 0
    Trust_level_5 = 0
    Trust_level_6 = 0

    if Trust_level == '2':
        Trust_level_2 = 1
    elif Trust_level == '3':
        Trust_level_3 = 1
    elif Trust_level == '4':
        Trust_level_4 = 1
    elif Trust_level == '5':
        Trust_level_5 = 1
    elif Trust_level == '6':
        Trust_level_5 = 1

    data = pd.concat([scaled_numeric_df, pd.DataFrame({
        'Trust_level_2': [Trust_level_2],
        'Trust_level_3': [Trust_level_3],
        'Trust_level_4': [Trust_level_4],
        'Trust_level_5': [Trust_level_5],
        'Trust_level_6': [Trust_level_6]
    })], axis=1)

    data = np.array(data).reshape(1,-1)

    # Make the prediction using the loaded model
    prediction = model.predict_proba(data)[:,1]
    prediction = prediction.item()
    prediction_percentage = "{:.2f}%".format(prediction * 100)

    # Render the prediction template with the result
    return render_template('index.html', prediction_text = 'Probability that the Transaction is Fraudulent {}'.format(prediction_percentage))

if __name__ == '__main__':
    app.run(debug=True, port=8000)