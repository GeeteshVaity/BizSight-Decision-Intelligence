import pandas as pd



def load_data(file_path) -> pd.DataFrame:
    #Load CSV file and return clean pandas DataFrame.
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise Exception('CSV not found.')
    

    
    #Handle missing values by replacing empty values with 0
    df["revenue"] = df["revenue"].fillna(0)
    df["cost"] = df["cost"].fillna(0)


    #Convert date
    df["date"] = pd.to_datetime(df["date"])

    return df