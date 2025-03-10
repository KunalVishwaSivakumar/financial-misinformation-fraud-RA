import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Load and preprocess the data
df = pd.read_csv('your_dataset.csv')  # Replace with your actual dataset path

# Example of encoding categorical variables, if any
# If you have categorical columns, you can encode them here, for example:
# df_encoded = pd.get_dummies(df, drop_first=True)

# Standardize numeric features
scaler = StandardScaler()
df_encoded = df.copy()  # Make a copy of the dataframe
numeric_cols = df.select_dtypes(include=[np.number]).columns  # Select only numeric columns
df_encoded[numeric_cols] = scaler.fit_transform(df_encoded[numeric_cols])

# Function to create sequences for LSTM input
def create_sequences(data, target_column, window_size):
    sequences = []
    labels = []
    
    # Exclude non-numeric columns (such as 'Date') before creating sequences
    data_numeric = data.select_dtypes(include=[np.number])  # Keep only numeric columns
    
    for i in range(len(data_numeric) - window_size):
        sequences.append(data_numeric.iloc[i:i + window_size].values.astype(np.float32))  # Explicitly convert to float32
        labels.append(data.iloc[i + window_size][target_column])  # Corresponding label
    
    return np.array(sequences), np.array(labels)

# Define your target column and window size
target_column = 'your_target_column_name'  # Replace with your actual target column
window_size = 10  # Adjust the window size as needed

# Create sequences and labels
X_seq, y_seq = create_sequences(df_encoded, target_column, window_size)

# Check the data types
print("X_seq dtype:", X_seq.dtype)
print("y_seq dtype:", y_seq.dtype)

# Split the data into training and testing sets
train_size = int(len(X_seq) * 0.8)
X_train, X_test = X_seq[:train_size], X_seq[train_size:]
y_train, y_test = y_seq[:train_size], y_seq[train_size:]

# Build the LSTM model
model = Sequential()
model.add(LSTM(64, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=20, batch_size=32)

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print(f"Test loss: {loss}")
