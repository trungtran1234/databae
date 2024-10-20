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

def generate_pie_chart(data):
    return
