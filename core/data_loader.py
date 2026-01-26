import pandas as pd

def load_data(file):
    try:
        if file is None:
            raise ValueError("No file uploaded")

        if file.size == 0:
            raise ValueError("Uploaded file is empty")

        # 🔥 THIS LINE GOES HERE (before read_csv)
        file.seek(0)

        # 🔥 Robust CSV read
        df = pd.read_csv(file, sep=None, engine="python")

        if df.empty:
            raise ValueError("CSV has no data")

        return df

    except Exception as e:
        raise Exception(f"Failed to read CSV: {e}")
