import matplotlib.pyplot as plt
import io
import base64
from IPython.display import Image, display

def display_pie_chart(base64_str):
    image_data = base64.b64decode(base64_str.split(',')[1])  # Remove the data:image/png;base64, prefix
    display(Image(data=image_data))

def save_pie_chart(base64_str, filename='pie_chart.png'):
    image_data = base64.b64decode(base64_str.split(',')[1])
    with open(filename, 'wb') as f:
        f.write(image_data)
    print(f"Pie chart saved as '{filename}'")

def generate_pie_chart(labels, values):
    """
    Generates a pie chart as a base64-encoded image.
    
    Args:
        labels (list): A list of labels for the pie chart.
        values (list): A list of values corresponding to the labels.
    
    Returns:
        str: A base64-encoded string of the generated pie chart.
    """
    print("IM IN PIE CHART TOOL")
    # Create a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the pie chart to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert to base64 for universal representation
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    # Clean up plt to prevent re-plotting issues
    plt.close()

    return f"data:image/png;base64,{image_base64}"


import pandas as pd

def generate_table(data):
    """
    Generates a table using the provided columns and rows.
    
    Args:
        columns (list): A list of column headers.
        rows (list): A list of lists where each inner list represents a row.
    
    Returns:
        str: A string representation of the table (or an HTML table).
    """
    # Create a DataFrame from the provided columns and rows
    df = pd.DataFrame(data)

    # Return the DataFrame as an HTML table or string table
    return df.to_html(index=False)  # You can change to to_string() if text output is desired.

from sklearn.linear_model import LinearRegression
import numpy as np

# Dummy data for training (for demonstration purposes)
training_data_X = np.array([[1], [2], [3], [4], [5]])
training_data_Y = np.array([2, 4, 6, 8, 10])

# Train a basic linear regression model (this can be extended)
model_mapping = {
    'linear_regression': LinearRegression().fit(training_data_X, training_data_Y)
}

def predict_data(data, model_name):
    """
    Provides a prediction using the specified model.
    
    Args:
        data (list): A list of input data for prediction.
        model_name (str): The predictive model to use (e.g., 'linear_regression').
    
    Returns:
        list: The predicted results.
    """
    if model_name not in model_mapping:
        return f"Model '{model_name}' is not supported."
    
    model = model_mapping[model_name]
    
    # Convert the data into the expected format (2D array)
    input_data = np.array(data).reshape(-1, 1)
    
    # Make predictions
    predictions = model.predict(input_data)
    
    return predictions.tolist()



