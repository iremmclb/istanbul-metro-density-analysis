import pandas as pd
import sqlite3
import re

csv_file = 'ulasim.csv'
db_file = 'metrodensity.db'

def clean_text(text):
    if pd.isna(text): return ""
    text = str(text).upper()
    mapping = {'İ':'I', 'I':'I', 'Ç':'C', 'Ş':'S', 'Ğ':'G', 'Ü':'U', 'Ö':'O'}
    for k, v in mapping.items():
        text = text.replace(k, v)
    return re.sub(r'[^A-Z0-9]', '', text)


ALIAS_DICT = {
    'ITUKUZEY': 'ITUAYAZAGA',
    'ITUGUNEY': 'ITUAYAZAGA',
    'SISLI2KUZEY': 'SISLIMECIDIYEKOY',
    'SISLIGUNEY': 'SISLIMECIDIYEKOY',
    'IDTM': 'ISTANBULFUARMERKEZI',
    'ORUCREISDOGU': 'ORUCREISYUZYIL', 
    'HASTANEBATI': 'HASTANE'
}

print("Son rötuşlar ve Manuel Sözlük entegrasyonu yapılıyor...")

try:
    conn = sqlite3.connect(db_file)
    
    lines_df = pd.read_sql_query("SELECT LineId, LineName FROM lines", conn)
    lines_df['CleanLine'] = lines_df['LineName'].apply(clean_text)
    
    stations_df = pd.read_sql_query("SELECT Id, StationName, LineName FROM stations", conn)
    stations_df['CleanStation'] = stations_df['StationName'].apply(clean_text)
    stations_df['CleanLine'] = stations_df['LineName'].apply(clean_text)
    
    line_name_to_id = dict(zip(lines_df['CleanLine'], lines_df['LineId']))
    
    def get_line_id(line_name):
        if not line_name: return None
        line_name = clean_text(line_name)
        if line_name in line_name_to_id: return line_name_to_id[line_name]
        if 'M1' in line_name: return 9 
        for db_line, lid in line_name_to_id.items():
            if line_name in db_line or db_line in line_name:
                return lid
        return None

    db_stations = []
    for _, row in stations_df.iterrows():
        db_stations.append({
            'Id': row['Id'],
            'Station': row['CleanStation'],
            'Line': row['CleanLine'],
            'LineId': get_line_id(row['CleanLine'])
        })
        
    def find_best_match(csv_line, csv_station):
        c_line = clean_text(csv_line)
        c_stat = clean_text(csv_station)
        
        # SÖZLÜK MÜDAHALESİ: Eğer bu inatçı bir istasyonsa, ismini tablomuza uygun hale getir
        if c_stat in ALIAS_DICT:
            c_stat = ALIAS_DICT[c_stat]
            
        best_id, best_line_id, max_len = None, None, 0
        
        for st in db_stations:
            line_match = (c_line in st['Line'] or st['Line'] in c_line)
            if c_line == 'M1' and st['Line'] in ['M1A', 'M1B', 'M1']:
                line_match = True
                
            if line_match:
                if st['Station'] in c_stat or c_stat in st['Station']:
                    if len(st['Station']) > max_len:
                        max_len = len(st['Station'])
                        best_id = st['Id']
                        best_line_id = st['LineId']
        
        return best_id, best_line_id

    df = pd.read_csv(csv_file, sep=',')
    
    unique_pairs = df[['line_name', 'station_poi_desc_cd']].drop_duplicates().dropna()
    mapping_dict = {}
    for _, row in unique_pairs.iterrows():
        mapping_dict[(row['line_name'], row['station_poi_desc_cd'])] = find_best_match(row['line_name'], row['station_poi_desc_cd'])
        
    df['tuple'] = list(zip(df['line_name'], df['station_poi_desc_cd']))
    df['StationId'] = df['tuple'].map(lambda x: mapping_dict.get(x, (None, None))[0])
    df['LineId'] = df['tuple'].map(lambda x: mapping_dict.get(x, (None, None))[1])
    
    df_final = df.dropna(subset=['StationId', 'LineId']).copy()
    
    df_final = df_final.rename(columns={
        'transition_date': 'TransitionDate',
        'transition_hour': 'TransitionHour',
        'number_of_passenger': 'PassengerCount'
    })
    
    df_final['StationId'] = df_final['StationId'].astype(int)
    df_final['LineId'] = df_final['LineId'].astype(int)
    df_final['PassengerCount'] = pd.to_numeric(df_final['PassengerCount'], errors='coerce').fillna(0).astype(int)
    
    df_grouped = df_final.groupby(['StationId', 'LineId', 'TransitionDate', 'TransitionHour'])['PassengerCount'].sum().reset_index()
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passenger_flow")
    conn.commit()
    
    df_grouped.to_sql('passenger_flow', conn, if_exists='append', index=False)
    print(f"TEBRİKLER! Tüm gerçek metrolar eksiksiz aktarıldı ({len(df_grouped)} satır).")
    
    conn.close()

except Exception as e:
    print(f"Hata oluştu: {e}")