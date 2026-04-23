import sqlite3

def mark_special_events():
    conn = sqlite3.connect('metrodensity.db')
    cursor = conn.cursor()

    #Official holidays and special events between Aug 2024 - Aug 2025
    holidays = [
        '2024-08-30', # Victory Day
        '2024-10-29', # Republic Day
        '2025-01-01', # New Year's Day
        '2025-03-30', # Ramadan Feast (Day 1)
        '2025-03-31', # (Day 2)
        '2025-04-01', # (Day 3)
        '2025-04-23', # National Sovereignty and Children's Day
        '2025-05-01', # Labor and Solidarity Day
        '2025-05-19', # Commemoration of Ataturk, Youth and Sports Day
        '2025-06-06', # Eid Qurban (Day 1)
        '2025-06-07', # (Day 2)
        '2025-06-08', # (Day 3)
        '2025-06-09', # (Day 4)
        '2025-07-15', # Democracy and National Unity Day
        '2025-08-30'  # Victory Day
    ]

    for holiday_date in holidays:
        cursor.execute("""
            UPDATE Calendar 
            SET IsSpecialEvent = 1 
            WHERE Date = ?
        """, (holiday_date,))

    conn.commit()
    print(f"Successfully marked {len(holidays)} special events in the Calendar table.")
    conn.close()

if __name__ == "__main__":
    mark_special_events()