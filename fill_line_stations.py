import sqlite3

def fill_line_stations():
    conn = sqlite3.connect('metrodensity.db')
    cursor = conn.cursor()

    cursor.execute("SELECT Id, LineName FROM stations ORDER BY LineName, Id")
    stations = cursor.fetchall()

    current_line = ""
    order_counter = 1

    for station in stations:
        s_id = station[0]
        line_name = station[1]
        
        if line_name != current_line:
            current_line = line_name
            order_counter = 1
        else:
            order_counter += 1
            
        cursor.execute("""
            UPDATE Line_Stations 
            SET StationOrder = ? 
            WHERE LineId = ? AND StationId = ?
        """, (order_counter, line_name, s_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fill_line_stations()