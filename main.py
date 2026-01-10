from core.data_loader import load_data
from core.data_validator import validate_dataframe
from data import *

df = load_data("data/sample_data.csv")
clean_df = validate_dataframe(df)

print(clean_df.head())
print(clean_df.info())