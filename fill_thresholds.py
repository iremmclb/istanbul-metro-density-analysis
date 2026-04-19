import sqlite3

def fill_thresholds():
    conn = sqlite3.connect('metrodensity.db')
    cursor = conn.cursor()

    cursor.execute("SELECT Id FROM stations")
    stations = cursor.fetchall()

    thresholds_data = []

    for station in stations:
        s_id = station[0]
        thresholds_data.append((s_id, 1500, 'Low'))
        thresholds_data.append((s_id, 4000, 'Medium'))
        thresholds_data.append((s_id, 10000, 'High'))

    cursor.execute("DELETE FROM Crowd_Thresholds")
    cursor.executemany(
        "INSERT INTO Crowd_Thresholds (StationId, UpperLimit, StatusLevel) VALUES (?, ?, ?)",
        thresholds_data
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fill_thresholds()