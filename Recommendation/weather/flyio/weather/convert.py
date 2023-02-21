from pandas import read_csv
from pickle import dump
from glob import glob
from tqdm import tqdm

HEADERS = ["DATE", "NAME", "LATITUDE", "LONGITUDE", "MIN", "MAX", "PRCP", "PRCP_ATTRIBUTES", "SNDP", "FRSHTT"]
TYPES = {"NAME": str, "LATITUDE": float, "LONGITUDE": float, "MIN": float, "MAX": float, "PRCP": float, "PRCP_ATTRIBUTES": str, "SNDP": float, "FRSHTT": str}

data = []

files = glob('stations/*.csv')
for i, file in enumerate(tqdm(files)):
    df = read_csv(file, dtype=TYPES, parse_dates=["DATE"])[HEADERS]
    # Ignore any stations without a name
    if df["NAME"].isnull().any():
        continue
    # Convert to dictionary for faster operations
    df = df.to_dict()
    data.append(df)

with open('weather.pickle', 'wb') as f:
    dump(data, f)
