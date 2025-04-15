import pandas as pd

def process_crime_data(file_path):
    try:
        # Load the CSV
        df = pd.read_csv(file_path)
        print(f"Columns in CSV: {df.columns.tolist()}")  # Debug: Show columns
        
        # Standardize column names
        df.columns = df.columns.str.upper().str.strip()
        
        # Define identifier columns
        id_vars = ['STATE/UT', 'YEAR']
        if not all(col in df.columns for col in id_vars):
            raise ValueError("Required columns 'STATE/UT' and 'YEAR' not found in CSV.")
        
        # Define crime columns (exclude identifiers and total)
        crime_columns = [col for col in df.columns if col not in id_vars and col != 'TOTAL IPC CRIMES']
        
        # Melt the wide format into long format
        df_long = pd.melt(
            df,
            id_vars=id_vars,
            value_vars=crime_columns,
            var_name='CRIME_TYPE',
            value_name='COUNT'
        )
        
        # Clean up
        df_long.dropna(subset=['STATE/UT', 'YEAR', 'CRIME_TYPE', 'COUNT'], inplace=True)
        df_long['STATE/UT'] = df_long['STATE/UT'].str.title()
        df_long['YEAR'] = df_long['YEAR'].astype(int)
        df_long['COUNT'] = df_long['COUNT'].astype(int)
        
        print(f"Processed DataFrame head:\n{df_long.head()}")  # Debug: Show result
        return df_long
    except Exception as e:
        print(f"Data processing error: {str(e)}")
        return None