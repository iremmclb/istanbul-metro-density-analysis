import pandas as pd
import sqlite3
import os

csv_file = 'ulasim.csv'
db_file = 'metrodensity.db'


try:
    df = pd.read_csv(csv_file, sep=',') 

    mapping = {
        'transition_date': 'TransitionDate',
        'transition_hour': 'TransitionHour',
        'line_name': 'LineId',
        'station_poi_desc_cd': 'StationId',
        'number_of_passenger': 'PassengerCount'
    }

    df_final = df[list(mapping.keys())].rename(columns=mapping)

    conn = sqlite3.connect(db_file)
    df_final.to_sql('passenger_flow', conn, if_exists='append', index=False)
    
    print(f"{len(df_final)} satır veri 'passenger_flow' tablosuna eklendi.")
    conn.close()

except Exception as e:
    print(f"Hata: {e}")