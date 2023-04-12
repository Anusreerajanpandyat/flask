from flask import Flask, jsonify, request
import pickle
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

# Load the trained KMeans model
with open('C:/Users/243415/Documents/flaskdocumentation/sree/models/scaledmodel.pkl', 'rb') as file:
    kmeans = pickle.load(file)

# Load the list of BSSIDs to include in the model
bssids =['24:f2:7f:34:88:f0', '24:f2:7f:34:88:f1', '24:f2:7f:34:88:f2','24:f2:7f:34:88:f4', '24:f2:7f:34:88:f5', '24:f2:7f:34:8c:f0',
   '24:f2:7f:34:8c:f1', '24:f2:7f:34:8c:f2', '24:f2:7f:34:8c:f3','24:f2:7f:34:8c:f4', '24:f2:7f:34:8d:10', '24:f2:7f:34:8d:11',
    '24:f2:7f:34:8d:12', '24:f2:7f:34:8d:14', '24:f2:7f:34:8d:15','24:f2:7f:34:8d:b0', '24:f2:7f:34:8d:b1', '24:f2:7f:34:8d:b2',
    '24:f2:7f:34:8d:b4', '24:f2:7f:34:8d:b5', '24:f2:7f:34:8e:91','24:f2:7f:34:8e:92', '24:f2:7f:34:8f:d0', '24:f2:7f:34:8f:d1',
    '24:f2:7f:34:8f:d2', '24:f2:7f:34:8f:d4', '24:f2:7f:34:8f:d5','24:f2:7f:34:95:70', '24:f2:7f:34:95:71', '24:f2:7f:34:95:b0',
    '24:f2:7f:34:96:90', '24:f2:7f:34:96:91', '24:f2:7f:34:96:92','24:f2:7f:34:96:94', '24:f2:7f:34:96:95', '24:f2:7f:34:9a:70',
    '24:f2:7f:34:9a:71', '24:f2:7f:34:9a:72', '24:f2:7f:34:9a:73','24:f2:7f:34:9a:74']

# Define the Flask application
app = Flask(__name__)

# Define the endpoint for the API
@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file was uploaded
    if len(request.files) == 0:
        return jsonify({'error': 'no file found'})

    # Get the uploaded file from the request
    uploaded_file = next(iter(request.files.values()))

    # Load the data from the uploaded file into a Pandas DataFrame
    try:
        data = pd.read_csv(uploaded_file)
    
        # Filter the data to only include BSSIDs in the list
        data = data[data['BSSID'].isin(bssids)]

        # Filter data22 to only include BSSIDs not in data11
        data_filtered = data[~data['BSSID'].isin(bssids)]
            
                # Create a DataFrame with all the BSSIDs in data11 that are not already in data22
        missing_bssids = pd.DataFrame({'BSSID': list(bssids- set(data['BSSID']))})
        missing_bssids['Location'] = data['Location'].iloc[0]
            
                # Concatenate the filtered data22 and the missing_bssids DataFrame
        data_complete = pd.concat([data_filtered, missing_bssids], ignore_index=True)
            
                # Fill in any missing values with 0
        data_complete.fillna(-200, inplace=True)
        data_new = pd.concat([data, data_complete], ignore_index=True)
            
        tabletest_pivot= pd.pivot_table(data=data_new,index=('Location'),columns=('BSSID'),values='Level', fill_value=-200)
        test_pivot =tabletest_pivot.reset_index()
        X_test=test_pivot.drop(['Location'], axis=1)
        Test= normalize(X_test)
        Test = pd.DataFrame(Test, columns=X_test.columns)
        
        
        # Make the predictions
        predictions = kmeans.predict(Test)
    
        # Return the predictions as a JSON response
        return jsonify({'predictions': predictions.tolist()})

    except Exception as e:
        return jsonify({'error': 'failed to load file: {}'.format(str(e))})

if __name__ == '__main__':
    app.run(port=5099, debug=True)
