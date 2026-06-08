import sqlite3
import time
import random
from datetime import datetime

DB_NAME = "metrodensity.db" 

def connect_db():
    return sqlite3.connect(DB_NAME)

def setup_database_requirements():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bottleneck_alerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id INT,
            log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            passenger_count INT,
            action_required VARCHAR(255)
        )
    """)
    
    cursor.execute("DROP VIEW IF EXISTS v_station_density_report")
    
    try:
        cursor.execute("""
            CREATE VIEW v_station_density_report AS
            SELECT 
                s.StationName,
                s.LineName,
                pf.PassengerCount,
                pf.TransitionDate,
                pf.TransitionHour
            FROM passenger_flow pf
            JOIN stations s ON pf.StationId = s.Id;
        """)
    except sqlite3.OperationalError:
        pass 
        
    conn.commit()
    conn.close()

def search_station():
    print("\n  STATION SEARCH ")
    keyword = input("Enter station name (press Enter to see all): ").strip().upper()
    
    conn = connect_db()
    cursor = conn.cursor()
    
    query = """
        SELECT DISTINCT Id, StationName, LineName 
        FROM stations 
        WHERE UPPER(StationName) LIKE ?
        ORDER BY Id ASC
    """
    cursor.execute(query, ('%' + keyword + '%',))
    rows = cursor.fetchall()
    
    if not rows:
        print("Warning: No stations found matching your criteria.")
    else:
        print(f"\n{'ID':<5} | {'Station Name':<25} | {'Line':<10}")
        print("-" * 45)
        for row in rows:
            print(f"{row[0]:<5} | {row[1]:<25} | {row[2]:<10}")
            
    conn.close()
    time.sleep(1)

def view_density_report():
    print("\n  STATION DENSITY REPORT ")
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT StationName, LineName, PassengerCount, TransitionDate, TransitionHour FROM v_station_density_report ORDER BY TransitionDate DESC, TransitionHour DESC LIMIT 20")
        rows = cursor.fetchall()
        
        print(f"{'Station Name':<20} | {'Line':<6} | {'Count':<8} | {'Date':<12} | {'Hour':<5}")
        print("-" * 62)
        for row in rows:
            print(f"{row[0]:<20} | {row[1]:<6} | {row[2]:<8} | {row[3]:<12} | {row[4]:<5}")
    except sqlite3.OperationalError as e:
        print(f"Warning: Error fetching report. Details: {e}")
        
    conn.close()
    time.sleep(1)

def simulate_passenger_entry():
    print("\n  NEW PASSENGER ENTRY SIMULATION ")
    try:
        station_id = int(input("Enter Station ID: "))
        passenger_count = int(input("Enter the current passenger count: "))
        
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        current_hour = int(now.strftime('%H'))

        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO passenger_flow (StationId, PassengerCount, TransitionDate, TransitionHour)
            VALUES (?, ?, ?, ?)
        """, (station_id, passenger_count, current_date, current_hour))
            
        conn.commit()
        print(f"Success! {passenger_count} passengers sent to database. (DB Trigger is monitoring...)")
        conn.close()
    except ValueError:
        print("Error: Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")
    time.sleep(1)

def check_bottleneck_alerts():
    print("\n  SYSTEM ALERTS AND BOTTLENECKS ")
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT a.log_time, s.StationName, a.passenger_count, a.action_required 
            FROM bottleneck_alerts a
            JOIN stations s ON a.station_id = s.Id
            ORDER BY a.log_time DESC
        """)
        rows = cursor.fetchall()
        
        if not rows:
            print("Everything is running. No critical density records found.")
        else:
            for row in rows:
                print(f"[{row[0]}] Station: {row[1]} | Passengers: {row[2]}")
                print(f"   ACTION: {row[3]}\n")
    except sqlite3.OperationalError as e:
        print(f"Error reading alerts. Details: {e}")
            
    conn.close()
    time.sleep(1)

def run_auto_daily_simulation():
    print("\n" + "="*50)
    print("   MATRIX MODE: AUTO RUSH HOUR SIMULATOR")
    print("="*50)
    print("Simulating a full day (06:00 to 23:00)...")
    time.sleep(1)
    
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.Id, s.StationName, c.UpperLimit 
        FROM stations s 
        JOIN Crowd_Thresholds c ON s.Id = c.StationId 
        WHERE c.UpperLimit > 500 
        LIMIT 5
    """)
    stations = cursor.fetchall()
    
    if not stations:
        print("Error: Could not find valid threshold data. Run your SQL update first.")
        conn.close()
        return

    current_date = datetime.now().strftime('%Y-%m-%d')
    
    for hour in range(6, 24):
        print(f"\n--- TIME: {hour:02d}:00 ---")
        for st in stations:
            st_id, st_name, limit = st
            
            if hour in [8, 9, 17, 18, 19]:
                passenger_count = int(limit * random.uniform(0.8, 1.2))
            else:
                passenger_count = int(limit * random.uniform(0.1, 0.4))
                
            cursor.execute("""
                INSERT INTO passenger_flow (StationId, PassengerCount, TransitionDate, TransitionHour)
                VALUES (?, ?, ?, ?)
            """, (st_id, passenger_count, current_date, hour))
            
            print(f"  -> {st_name}: {passenger_count} passengers entered.")
                
        time.sleep(0.8) 
        
    conn.commit()
    conn.close()
    print("\n  SIMULATION COMPLETE ")
    print("Check Option 4 (Alerts) to see the DB Trigger in action!")
    time.sleep(2)

def main_menu():
    setup_database_requirements()
    
    while True:
        print("\n" + "="*50)
        print("   ISTANBUL SUBWAY DENSITY MONITORING SYSTEM   ")
        print("="*50)
        print("1. Search for Station IDs")
        print("2. View Station Density Report")
        print("3. Enter New Passenger Data (Manual)")
        print("4. Check Bottleneck Alerts")
        print("5. Run Auto Daily Simulation (RUSH HOUR)")
        print("6. Exit")
        
        choice = input("Please select an operation (1-6): ")
        
        if choice == '1':
            search_station()
        elif choice == '2':
            view_density_report()
        elif choice == '3':
            simulate_passenger_entry()
        elif choice == '4':
            check_bottleneck_alerts()
        elif choice == '5':
            run_auto_daily_simulation()
        elif choice == '6':
            print("Exiting system. Have a great day!")
            break
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main_menu()