import pandas as pd

requiredColumns = {"date","product","revenue","cost"}

def load_data(file_path):
    #Load CSV file and return clean pandas DataFrame.
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise Exception('CSV not found.')
    
    #Validate columns
    if not requiredColumns.issubset(df.columns):
        missing = requiredColumns - set(df.columns)
        raise Exception(f"Missing column: {missing}")
    
    #Handle missing values
    df["revenue"] = df["revenue"].fillna(0)
    df["cost"] = df["cost"].fillna(0)


    #Convert date
    df["date"] = pd.to_datetime(df["date"])

    return df