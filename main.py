import sqlite3

class DBOperations:
  sql_create_destinations = """
    CREATE TABLE IF NOT EXISTS Destinations (
      DestinationID   INTEGER PRIMARY KEY AUTOINCREMENT,
      City            TEXT    NOT NULL,
      Country         TEXT    NOT NULL,
      AirportCode     TEXT    NOT NULL UNIQUE,
      AirportName     TEXT    NOT NULL,
      Timezone        TEXT    NOT NULL
        )
    """

  sql_create_pilots = """
    CREATE TABLE IF NOT EXISTS Pilots (
      PilotID         INTEGER PRIMARY KEY AUTOINCREMENT,
      FirstName       TEXT    NOT NULL,
      LastName        TEXT    NOT NULL,
      LicenseNumber   TEXT    NOT NULL UNIQUE,
      Rank            TEXT    NOT NULL,
      FlightHours     INTEGER NOT NULL
        )
    """

  sql_create_flights = """
      CREATE TABLE IF NOT EXISTS Flights (
          FlightID        INTEGER PRIMARY KEY,
          Origin          TEXT    NOT NULL,
          DestinationID   INTEGER NOT NULL,
          DepartureDate   TEXT    NOT NULL,
          DepartureTime   TEXT    NOT NULL,
          ArrivalTime     TEXT    NOT NULL,
          Status          TEXT    NOT NULL DEFAULT 'Scheduled',
          PilotID         INTEGER,
          FOREIGN KEY (DestinationID) REFERENCES Destinations(DestinationID),
          FOREIGN KEY (PilotID)       REFERENCES Pilots(PilotID)
        )
    """

  # Sample destination data
  sample_destinations = [
      (1111, "New York", "USA", "JFK", "John F. Kennedy International Airport", "UTC-5"),
      (1112, "London", "UK", "LHR", "Heathrow Airport", "UTC+0"),
      (1113, "Paris", "France", "CDG", "Charles de Gaulle Airport", "UTC+1"),
      (1114, "Tokyo", "Japan", "NRT", "Narita International Airport", "UTC+9"),
      (1115, "Sydney", "Australia", "SYD", "Sydney Kingsford Smith Airport", "UTC+10"),
      (1116, "Dubai", "UAE", "DXB", "Dubai International Airport", "UTC+4"),
      (1117, "Singapore", "Singapore", "SIN", "Changi Airport", "UTC+8"),
      (1118, "Frankfurt", "Germany", "FRA", "Frankfurt Airport", "UTC+1"),
      (1119, "Hong Kong", "China", "HKG", "Hong Kong International Airport", "UTC+8"),
      (1120, "Los Angeles", "USA", "LAX", "Los Angeles International Airport", "UTC-8"),
      (1121, "Chicago", "USA", "ORD", "O'Hare International Airport", "UTC-6"),
      (1122, "Miami", "USA", "MIA", "Miami International Airport", "UTC-5"),
      (1123, "Amsterdam", "Netherlands", "AMS", "Amsterdam Schiphol Airport", "UTC+1"),
      (1124, "Seoul", "South Korea", "ICN", "Incheon International Airport", "UTC+9"),
      (1125, "Bangkok", "Thailand", "BKK", "Suvarnabhumi Airport", "UTC+7")
    ]

  # Sample pilot data
  sample_pilots = [
      (1, "John", "Smith", "LN12345", "Captain", 5000),
      (2, "Emily", "Johnson", "LN54321", "First Officer", 3000),
      (3, "Michael", "Brown", "LN67890", "Captain", 7000),
      (4, "Sarah", "Davis", "LN09876", "First Officer", 4000),
      (5, "David", "Wilson", "LN11223", "Captain", 6000),
      (6, "Jessica", "Miller", "LN33211", "First Officer", 3500),
      (7, "Daniel", "Garcia", "LN44556", "Captain", 8000),
      (8, "Laura", "Martinez", "LN66554", "First Officer", 2500),
      (9, "James", "Anderson", "LN77889", "Captain", 9000),
      (10, "Olivia", "Taylor", "LN99887", "First Officer", 4500),
      (11, "Robert", "Thomas", "LN55667", "Captain", 7500),
      (12, "Sophia", "Moore", "LN66778", "First Officer", 2000),
      (13, "William", "Jackson", "LN88990", "Captain", 8500),
      (14, "Ava", "White", "LN99000", "First Officer", 3000),
      (15, "James", "Harris", "LN22334", "Captain", 6500)
  ]

  # Sample flight data
  sample_flights = [
    (101, "Seoul (ICN)", 1111, "2026-07-01", "08:00", "11:00", "On Time", 1),
    (102, "Seoul (ICN)", 1112, "2026-07-02", "09:00", "14:00", "Delayed", 2),
    (103, "Tokyo (NRT)", 1113, "2026-07-03", "10:00", "13:30", "Cancelled", 3),
    (104, "London (LHR)", 1114, "2026-07-04", "11:00", "23:00", "On Time", 4),
    (105, "Dubai (DXB)", 1115, "2026-07-05", "12:00", "22:00", "Delayed", 5),
    (106, "New York (JFK)", 1116, "2026-07-06", "13:00", "19:00", "On Time", 6),
    (107, "Paris (CDG)", 1117, "2026-07-07", "14:00", "21:00", "Cancelled", 7),
    (108, "Bangkok (BKK)", 1118, "2026-07-08", "15:00", "18:00", "On Time", 8),
    (109, "Los Angeles (LAX)", 1119, "2026-07-09", "16:00", "20:00", "Delayed", 9),
    (110, "Sydney (SYD)", 1120, "2026-07-10", "17:00", "23:30", "On Time", 10),
    (111, "Frankfurt (FRA)", 1121, "2026-07-11", "18:00", "21:00", "Cancelled", 11),
    (112, "Singapore (SIN)", 1122, "2026-07-12", "19:00", "22:30", "On Time", 12),
    (113, "Amsterdam (AMS)", 1123, "2026-07-13", "07:00", "10:00", "Delayed", 13),
    (114, "Chicago (ORD)", 1124, "2026-07-14", "08:30", "11:30", "On Time", 14),
    (115, "Miami (MIA)", 1125, "2026-07-15", "09:00", "12:00", "Cancelled", 15),
    ]

  # Connect to database and create tables
  def __init__(self):
    try:
      self.conn = sqlite3.connect("DBName.db")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_destinations)
      self.cur.execute(self.sql_create_pilots)
      self.cur.execute(self.sql_create_flights)
      self.conn.commit()
      print("Database connected and tables created successfully")
    except Exception as e:
      print("Connecting to database or creating tables failed: " + str(e))
    finally:
      self.conn.close()

  # Open a new database connection
  def get_connection(self):
    self.conn = sqlite3.connect("DBName.db")
    self.cur = self.conn.cursor()

  # Insert sample data into all three tables
  def load_sample_data(self):
    try:
      self.get_connection()
      self.cur.executemany("INSERT OR IGNORE INTO Destinations (DestinationID, City, Country, AirportCode, AirportName, Timezone) VALUES (?, ?, ?, ?, ?, ?)", self.sample_destinations)
      self.cur.executemany("INSERT OR IGNORE INTO Pilots (PilotID, FirstName, LastName, LicenseNumber, Rank, FlightHours) VALUES (?, ?, ?, ?, ?, ?)", self.sample_pilots)
      self.cur.executemany("INSERT OR IGNORE INTO Flights (FlightID, Origin, DestinationID, DepartureDate, DepartureTime, ArrivalTime, Status, PilotID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", self.sample_flights)
      self.conn.commit()
      print("Sample data loaded successfully")
    except Exception as e:
      print("Loading sample data failed: " + str(e))
    finally:
      self.conn.close()


class FlightOperation:

  # Open a new database connection
  def get_connection(self):
    self.conn = sqlite3.connect("DBName.db")
    self.cur = self.conn.cursor()

  # Helper: validate that a FlightID exists in the database
  def flight_exists(self, flight_id):
    self.cur.execute("SELECT FlightID FROM Flights WHERE FlightID = ?", (flight_id,))
    return self.cur.fetchone() is not None

  # Helper: validate that a PilotID exists in the database
  def pilot_exists(self, pilot_id):
    self.cur.execute("SELECT PilotID FROM Pilots WHERE PilotID = ?", (pilot_id,))
    return self.cur.fetchone() is not None

  # Helper: validate that a DestinationID exists in the database
  def destination_exists(self, dest_id):
    self.cur.execute("SELECT DestinationID FROM Destinations WHERE DestinationID = ?", (dest_id,))
    return self.cur.fetchone() is not None

  # Helper: validate date format YYYY-MM-DD
  def valid_date(self, date_str):
    import re
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_str))

  # Helper: validate time format HH:MM
  def valid_time(self, time_str):
    import re
    return bool(re.match(r"^\d{2}:\d{2}$", time_str))

  # Add a new flight with full input validation
  def add_flight(self):
    try:
      self.get_connection()
      print("\nEnter flight details:")

      # Validate Flight ID - must be an integer and not already exist
      while True:
        try:
          flight_id = int(input("Flight ID (number): "))
          if self.flight_exists(flight_id):
            print("Flight ID already exists. Please enter a different ID.")
          else:
            break
        except ValueError:
          print("Invalid input. Please enter a number.")

      origin = input("Origin: ").strip()
      while not origin:
        print("Origin cannot be empty.")
        origin = input("Origin: ").strip()

      # Show available destinations and validate DestinationID
      print("\nAvailable Destinations:")
      self.cur.execute("SELECT DestinationID, City, Country FROM Destinations ORDER BY City")
      for row in self.cur.fetchall():
        print(f"{row[0]} - {row[1]}, {row[2]}")
      while True:
        try:
          dest_id = int(input("Destination ID: "))
          if self.destination_exists(dest_id):
            break
          else:
            print("Destination ID not found. Please choose from the list above.")
        except ValueError:
          print("Invalid input. Please enter a number.")

      # Validate departure date format
      while True:
        depart_date = input("Departure Date (YYYY-MM-DD): ").strip()
        if self.valid_date(depart_date):
          break
        print("Invalid date format. Please use YYYY-MM-DD (e.g. 2026-07-01).")

      # Validate departure time format
      while True:
        depart_time = input("Departure Time (HH:MM): ").strip()
        if self.valid_time(depart_time):
          break
        print("Invalid time format. Please use HH:MM (e.g. 08:00).")

      # Validate arrival time format
      while True:
        arrive_time = input("Arrival Time (HH:MM): ").strip()
        if self.valid_time(arrive_time):
          break
        print("Invalid time format. Please use HH:MM (e.g. 11:00).")

      # Validate status value
      valid_statuses = ["Scheduled", "On Time", "Delayed", "Cancelled"]
      while True:
        status = input("Status (Scheduled / On Time / Delayed / Cancelled): ").strip()
        if status in valid_statuses:
          break
        elif status == "":
          status = "Scheduled"
          break
        else:
          print(f"  Invalid status. Please enter one of: {', '.join(valid_statuses)}")

      self.cur.execute(
        "INSERT INTO Flights VALUES (?,?,?,?,?,?,?,NULL)",
          (flight_id, origin, dest_id, depart_date, depart_time, arrive_time, status))
      self.conn.commit()
      print("Flight " + str(flight_id) + " added successfully.")

    except Exception as e:
      print("Error adding flight: " + str(e))
    finally:
      self.conn.close()

  # View flights filtered by destination, status, departure date, or all
  def view_flights_by_criteria(self):
    try:
      self.get_connection()
      print("\n View Flights by Criteria:")
      print("1. By Destination")
      print("2. By Status")
      print("3. By Departure Date")
      print("4. All Flights")
      choice = input("Select criteria (1-4): ").strip()

      if choice == '1':
        dest = input("Enter Destination City: ").strip() or None
        status = None
        depart_date = None
      elif choice == '2':
        valid_statuses = ["Scheduled", "On Time", "Delayed", "Cancelled"]
        while True:
          status = input("Enter Status (Scheduled / On Time / Delayed / Cancelled): ").strip()
          if status in valid_statuses:
            break
          print(f"Invalid status. Please enter one of: {', '.join(valid_statuses)}")
        dest = None
        depart_date = None
      elif choice == '3':
        while True:
          depart_date = input("Enter Departure Date (YYYY-MM-DD): ").strip()
          if self.valid_date(depart_date):
            break
          print("Invalid date format. Please use YYYY-MM-DD.")
        dest = None
        status = None
      else:
        dest = None
        status = None
        depart_date = None

      # Use JOIN to combine Flights and Destinations, filter by given criteria
      self.cur.execute("""
          SELECT f.FlightID, f.Origin, d.City, d.AirportCode, f.DepartureDate, f.DepartureTime, f.ArrivalTime, f.Status
          FROM Flights f
          JOIN Destinations d ON f.DestinationID = d.DestinationID
          WHERE (d.City LIKE ? OR ? IS NULL)
          AND (f.Status LIKE ? OR ? IS NULL)
          AND (f.DepartureDate = ? OR ? IS NULL)
          ORDER BY f.DepartureDate, f.DepartureTime
          """, (dest, dest, status, status, depart_date, depart_date))

      rows = self.cur.fetchall()
      if not rows:
        print("\n No flights found matching your criteria.")
        return
      print("\n " + "-" * 110)
      print(f"{'FlightID':<10} {'Origin':<20} {'Destination':<30} {'Date':<15} {'Dep':<10} {'Arr':<10} {'Status':<15}")
      print("-" * 110)
      for row in rows:
        print(f"{row[0]:<10} {row[1]:<20} {row[2]:<30} {row[3]:<15} {row[4]:<10} {row[5]:<10} {row[6]:<15}")
      print("-" * 110)
      print(f"Total: {len(rows)} flight(s)")

    except Exception as e:
      print("Error retrieving flights: " + str(e))
    finally:
      self.conn.close()

  # Update departure date, time, arrival time, or status for a specific flight
  def update_flight(self):
    try:
      self.get_connection()
      print("\nUpdate Flight Information:")

      # Validate FlightID exists
      while True:
        try:
          flight_id = int(input("Enter FlightID to update: "))
          if self.flight_exists(flight_id):
            break
          else:
            print("Flight ID not found. Please enter a valid Flight ID.")
        except ValueError:
          print("Invalid input. Please enter a number.")

      self.cur.execute("SELECT * FROM Flights WHERE FlightID = ?", (flight_id,))
      existing = self.cur.fetchone()

      print(f"Current Departure Date: {existing[3]}")
      while True:
        new_date = input("New Date (Enter to keep, YYYY-MM-DD): ").strip()
        if new_date == "":
          new_date = existing[3]
          break
        elif self.valid_date(new_date):
          break
        print("Invalid date format. Please use YYYY-MM-DD.")

      print(f"Current Departure Time: {existing[4]}")
      while True:
        new_dep = input("New Departure Time (Enter to keep, HH:MM): ").strip()
        if new_dep == "":
          new_dep = existing[4]
          break
        elif self.valid_time(new_dep):
          break
        print("Invalid time format. Please use HH:MM.")

      print(f"Current Arrival Time: {existing[5]}")
      while True:
        new_arr = input("New Arrival Time (Enter to keep, HH:MM): ").strip()
        if new_arr == "":
          new_arr = existing[5]
          break
        elif self.valid_time(new_arr):
          break
        print("Invalid time format. Please use HH:MM.")

      valid_statuses = ["Scheduled", "On Time", "Delayed", "Cancelled"]
      print(f"Current Status: {existing[6]}")
      while True:
        new_stat = input("New Status (Enter to keep): ").strip()
        if new_stat == "":
          new_stat = existing[6]
          break
        elif new_stat in valid_statuses:
          break
        print(f"Invalid status. Please enter one of: {', '.join(valid_statuses)}")

      self.cur.execute("""
        UPDATE Flights
        SET DepartureDate = ?, DepartureTime = ?, ArrivalTime = ?, Status = ?
        WHERE FlightID = ?
      """, (new_date, new_dep, new_arr, new_stat, flight_id))
      self.conn.commit()
      print("Flight " + str(flight_id) + " updated successfully.")

    except Exception as e:
      print("Updating flight failed: " + str(e))
    finally:
      self.conn.close()

  # Assign a pilot to a flight using UPDATE query
  def assign_pilot(self):
    try:
      self.get_connection()
      print("\nAssign Pilot to Flight:")

      # Validate FlightID exists
      while True:
        try:
          flight_id = int(input("Enter FlightID: "))
          if self.flight_exists(flight_id):
            break
          else:
            print("Flight ID not found. Please enter a valid Flight ID.")
        except ValueError:
          print("Invalid input. Please enter a number.")

      # Validate PilotID exists
      while True:
        try:
          pilot_id = int(input("Enter PilotID: "))
          if self.pilot_exists(pilot_id):
            break
          else:
            print("Pilot ID not found. Please enter a valid Pilot ID.")
        except ValueError:
          print("Invalid input. Please enter a number.")

      self.cur.execute("SELECT * FROM Pilots WHERE PilotID = ?", (pilot_id,))
      pilot = self.cur.fetchone()

      self.cur.execute("UPDATE Flights SET PilotID = ? WHERE FlightID = ?", (pilot_id, flight_id))
      self.conn.commit()
      print(f"Pilot {pilot[1]} {pilot[2]} assigned to Flight {flight_id} successfully.")

    except Exception as e:
      print("Assigning pilot failed: " + str(e))
    finally:
      self.conn.close()

  # View all flights assigned to a specific pilot using JOIN
  def view_pilot_schedule(self):
    try:
      self.get_connection()
      print("\nView Pilot Schedule")

      # Validate PilotID exists
      while True:
        try:
          pilot_id = int(input("Enter Pilot ID: "))
          if self.pilot_exists(pilot_id):
            break
          else:
            print("Pilot ID not found. Please enter a valid Pilot ID.")
        except ValueError:
          print("Invalid input. Please enter a number.")

      self.cur.execute("""
      SELECT p.FirstName, p.LastName, p.Rank, p.LicenseNumber, p.FlightHours
      FROM Pilots p WHERE p.PilotID = ?
      """, (pilot_id,))
      pilot = self.cur.fetchone()

      print(f"\nPilot: {pilot[0]} {pilot[1]} | {pilot[2]} | License: {pilot[3]} | Hours: {pilot[4]}")
      print("  " + "-" * 90)

      self.cur.execute("""
        SELECT f.FlightID, f.Origin, d.City, d.AirportCode,
               f.DepartureDate, f.DepartureTime, f.ArrivalTime, f.Status
        FROM Flights f
        JOIN Destinations d ON f.DestinationID = d.DestinationID
        WHERE f.PilotID = ?
        ORDER BY f.DepartureDate, f.DepartureTime
      """, (pilot_id,))
      flights = self.cur.fetchall()

      if not flights:
        print("No flights assigned to this pilot.")
        return

      print(f"{'FlightID':<10} {'Origin':<20} {'Destination':<18} {'Date':<12} {'Dep':<7} {'Arr':<7} {'Status'}")
      print("  " + "-" * 90)
      for r in flights:
        dest_str = r[2] + " (" + r[3] + ")"
        print(f"  {r[0]:<10} {r[1]:<20} {dest_str:<18} {r[4]:<12} {r[5]:<7} {r[6]:<7} {r[7]}")
      print("  " + "-" * 90)
      print(f"Total assigned flights: {len(flights)}")

    except Exception as e:
      print("Error viewing pilot schedule: " + str(e))
    finally:
      self.conn.close()

  # View all destinations or update a destination's city and country
  def view_update_destination(self):
    try:
      self.get_connection()
      print("\nView and Update Destination Information")
      print("1.View All Destinations")
      print("2.Update Destination")
      choice = input("Select option (1-2): ").strip()

      if choice == '1':
        self.cur.execute("SELECT * FROM Destinations ORDER BY City")
        rows = self.cur.fetchall()
        print("\n " + "-" * 140)
        print(f"{'ID':<5} {'City':<20} {'Country':<20} {'AirportCode':<15} {'AirportName':<25} {'Timezone':<10}")
        print("-" * 140)
        for row in rows:
          print(f" {row[0]:<5} {row[1]:<20} {row[2]:<20} {row[3]:<15} {row[4]:<25} {row[5]:<10}")
        print("-" * 140)

      elif choice == '2':
        # Validate DestinationID exists
        while True:
          try:
            des_id = int(input("Enter Destination ID to update: "))
            if self.destination_exists(des_id):
              break
            else:
              print("Destination ID not found. Please enter a valid ID.")
          except ValueError:
            print("Invalid input. Please enter a number.")

        self.cur.execute("SELECT * FROM Destinations WHERE DestinationID = ?", (des_id,))
        d = self.cur.fetchone()
        print(f"Current City: {d[1]}")
        new_city = input("New City (Enter to keep): ").strip() or d[1]
        print(f"Current Country: {d[2]}")
        new_country = input("New Country (Enter to keep): ").strip() or d[2]

        self.cur.execute("UPDATE Destinations SET City = ?, Country = ? WHERE DestinationID = ?", (new_city, new_country, des_id))
        self.conn.commit()
        print("Destination " + str(des_id) + " updated successfully.")
      else:
        print("Invalid option.")

    except Exception as e:
      print("Error viewing/updating destination: " + str(e))
    finally:
      self.conn.close()

  # Display summary statistics using COUNT and GROUP BY
  def view_summary_statistics(self):
    try:
      self.get_connection()
      print("\nSummary Statistics:")
      print("\n Flights per Destination:")
      self.cur.execute("""
        SELECT d.City, COUNT(f.FlightID) as TotalFlights
        FROM Flights f JOIN Destinations d ON f.DestinationID = d.DestinationID
        GROUP BY d.DestinationID
        ORDER BY TotalFlights DESC""")

      stats = self.cur.fetchall()
      for r in stats:
        print(f"{r[0]:<20} {r[1]} flight(s)")

      print("\n Flights per Pilot:")
      self.cur.execute("""
        SELECT p.FirstName || ' ' || p.LastName,
               COUNT(f.FlightID) as TotalFlights
        FROM Pilots p LEFT JOIN Flights f ON f.PilotID = p.PilotID
        GROUP BY p.PilotID
        ORDER BY TotalFlights DESC
      """)

      pilot_stats = self.cur.fetchall()
      print(f"{'Pilot':<20} {'Count':<10}")
      for s in pilot_stats:
        print(f"{s[0]:<20} {s[1]} flight(s)")

    except Exception as e:
      print("Error viewing summary statistics: " + str(e))
    finally:
      self.conn.close()

  # View all pilots ordered by last name
  def view_all_pilots(self):
    try:
      self.get_connection()
      print("\n All Pilots:")
      self.cur.execute("SELECT * FROM Pilots ORDER BY LastName")
      rows = self.cur.fetchall()
      print("\n " + "-" * 90)
      print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'License':<15} {'Rank':<16} {'Hours'}")
      print("-" * 90)
      for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<15} {row[4]:<16} {row[5]:<10}")
      print("-" * 90)
    except Exception as e:
      print("Error viewing pilots: " + str(e))
    finally:
      self.conn.close()


# Menu loop - user selects an option to interact with the database
def print_menu():
  print("\n Menu:")
  print("***********************************")
  print(" 1. Add a new flight")
  print(" 2. View all flights by criteria")
  print(" 3. Update flight information")
  print(" 4. Assign a pilot to a flight")
  print(" 5. View pilot schedule")
  print(" 6. View and update destination information")
  print(" 7. View summary statistics")
  print(" 8. View all pilots")
  print(" 9. Load sample data")
  print(" 10. Exit")

db = DBOperations()
ops = FlightOperation()

while True:
  print_menu()
  try:
    choice = int(input("Select an option (1-10): ").strip())
  except ValueError:
    print("Invalid input. Please enter a number between 1 and 10.")
    continue

  if choice == 1:
    ops.add_flight()
  elif choice == 2:
    ops.view_flights_by_criteria()
  elif choice == 3:
    ops.update_flight()
  elif choice == 4:
    ops.assign_pilot()
  elif choice == 5:
    ops.view_pilot_schedule()
  elif choice == 6:
    ops.view_update_destination()
  elif choice == 7:
    ops.view_summary_statistics()
  elif choice == 8:
    ops.view_all_pilots()
  elif choice == 9:
    db.load_sample_data()
  elif choice == 10:
    print("Exiting program. Goodbye!")
    break
  else:
    print("Invalid option. Please select a number between 1 and 10.")