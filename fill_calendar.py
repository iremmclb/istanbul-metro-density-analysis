import sqlite3
from datetime import date, timedelta


def fill_calendar():
    conn = sqlite3.connect('metrodensity.db')
    cursor = conn.cursor()

    start_date = date(2024, 8, 1)
    end_date = date(2025, 8, 31)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Calendar (
            Date TEXT PRIMARY KEY,
            DayName TEXT,
            IsWorkDay INTEGER,
            IsSpecialEvent INTEGER
        )
    """)
    current_date = start_date
    calendar_data = []

    while current_date <= end_date:

        date_str = current_date.strftime('%Y-%m-%d')

        day_name = current_date.strftime('%A')

        is_work_day = 1 if current_date.weekday() < 5 else 0

        is_special_event = 0 
        
        calendar_data.append((date_str, day_name, is_work_day, is_special_event))
        current_date += timedelta(days=1)

    cursor.executemany(
        "INSERT OR IGNORE INTO Calendar (Date, DayName, IsWorkDay, IsSpecialEvent) VALUES (?, ?, ?, ?)",
        calendar_data
    )

    conn.commit()
    print(f"{len(calendar_data)} günlük takvim verisi yüklendi")
    conn.close()

if __name__ == "__main__":
    fill_calendar()