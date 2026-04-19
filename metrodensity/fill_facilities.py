import sqlite3

def fill_facilities():
    conn = sqlite3.connect('metrodensity.db')
    cursor = conn.cursor()

    cursor.execute("SELECT Id FROM stations")
    stations = cursor.fetchall()

    facilities_data = []

    for station in stations:
        s_id = station[0]
        facilities_data.append((s_id, 'Asansör', 1))
        facilities_data.append((s_id, 'Yürüyen Merdiven', 1))

    cursor.execute("DELETE FROM Facilities")
    cursor.executemany(
        "INSERT INTO Facilities (StationId, FacilityType, Status) VALUES (?, ?, ?)",
        facilities_data
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fill_facilities()