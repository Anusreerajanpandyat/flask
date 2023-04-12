import os
import pandas as pd

from sklearn.preprocessing import normalize

# Path to the raw data directory

raw_data_dir = 'C:/Users/243415/Documents/flaskdocumentation/sree/data/raw'

# Path to the processed data directory
processed_data_dir = 'C:/Users/243415/Documents/flaskdocumentation/sree/data/processed'

# List all CSV files in the raw data directory
csv_files = [f for f in os.listdir(raw_data_dir) if f.endswith('.csv')]

# Process each CSV file and save the result in the processed data directory
for csv_file in csv_files:
    # Read the CSV file into a Pandas DataFrame
    data = pd.read_csv(os.path.join(raw_data_dir, csv_file))

    # Filter the data
    data = data[((data['Frequency'] > 5000) | data['Frequency'].isnull())]

    # Pivot the data
    bssids = ['24:f2:7f:34:88:f0', '24:f2:7f:34:88:f1', '24:f2:7f:34:88:f2','24:f2:7f:34:88:f4', '24:f2:7f:34:88:f5', '24:f2:7f:34:8c:f0',
   '24:f2:7f:34:8c:f1', '24:f2:7f:34:8c:f2', '24:f2:7f:34:8c:f3','24:f2:7f:34:8c:f4', '24:f2:7f:34:8d:10', '24:f2:7f:34:8d:11',
    '24:f2:7f:34:8d:12', '24:f2:7f:34:8d:14', '24:f2:7f:34:8d:15','24:f2:7f:34:8d:b0', '24:f2:7f:34:8d:b1', '24:f2:7f:34:8d:b2',
    '24:f2:7f:34:8d:b4', '24:f2:7f:34:8d:b5', '24:f2:7f:34:8e:91','24:f2:7f:34:8e:92', '24:f2:7f:34:8f:d0', '24:f2:7f:34:8f:d1',
    '24:f2:7f:34:8f:d2', '24:f2:7f:34:8f:d4', '24:f2:7f:34:8f:d5','24:f2:7f:34:95:70', '24:f2:7f:34:95:71', '24:f2:7f:34:95:b0',
    '24:f2:7f:34:96:90', '24:f2:7f:34:96:91', '24:f2:7f:34:96:92','24:f2:7f:34:96:94', '24:f2:7f:34:96:95', '24:f2:7f:34:9a:70',
    '24:f2:7f:34:9a:71', '24:f2:7f:34:9a:72', '24:f2:7f:34:9a:73','24:f2:7f:34:9a:74']
    data11 = data[data['BSSID'].isin(bssids)]
    tabletrain_pivot = pd.pivot_table(data=data11, index=('Location'), columns=('BSSID'), values='Level', fill_value=-200)
    train_pivot = tabletrain_pivot.reset_index()

    # Normalize the data
    X = train_pivot.drop(['Location'], axis=1)
    Train = normalize(X)
    Train = pd.DataFrame(Train, columns=X.columns)

    # Save the processed data as a CSV file
    output_file = csv_file.replace('.csv', '_processed.csv')
    Train.to_csv(os.path.join(processed_data_dir, output_file), index=False)

