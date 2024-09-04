from sqlite3 import connect

def initialize_bwc_database(db_name: str = 'gps_jobs.db'):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = connect(db_name)
    cursor = conn.cursor()

    # Create the Taxi table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Taxi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            primary_fleet TEXT NOT NULL,
            rego TEXT NOT NULL,
            rego_expiry DATE NOT NULL,
            coi_expiry DATE NOT NULL,
            fleets TEXT NOT NULL,
            conditions TEXT NOT NULL,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            build_date TEXT NOT NULL,
            pax INTEGER NOT NULL,
            validation TEXT,
            until DATE,
            reason TEXT
        )
    ''')

    # Create the Driver table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Driver (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER NOT NULL UNIQUE,
            name TEXT NOT NULL,
            greeting TEXT NOT NULL,
            address TEXT NOT NULL,
            suburb TEXT NOT NULL,
            post_code INTEGER NOT NULL,
            dob DATE NOT NULL,
            mobile TEXT NOT NULL,
            city TEXT NOT NULL,
            da_expiry DATE NOT NULL,
            license_expiry DATE NOT NULL,
            auth_wheelchair BOOLEAN,
            auth_bc BOOLEAN,
            auth_redcliffe BOOLEAN,
            auth_london BOOLEAN,
            auth_mandurah BOOLEAN,
            refer_fleet_ops BOOLEAN,
            conditions TEXT NOT NULL,
            create_date DATE NOT NULL,
            first_logon DATE NOT NULL,
            last_logon DATE NOT NULL,
            first_operator_logon DATE NOT NULL,
            logons_for_operator INTEGER NOT NULL,
            hours_for_operator INTEGER NOT NULL,
            validation_active BOOLEAN,
            validation_until DATE,
            validation_reason TEXT
        )
    ''')

    # Create the Shift table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shift (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER NOT NULL,
            driver_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            log_on DATETIME NOT NULL,
            log_off DATETIME NOT NULL,
            duration INTEGER NOT NULL,  -- Using TEXT to store timedelta as a string
            distance INTEGER NOT NULL,
            offered INTEGER NOT NULL,
            accepted INTEGER NOT NULL,
            rejected INTEGER NOT NULL,
            recalled INTEGER NOT NULL,
            completed INTEGER NOT NULL,
            total_fares REAL NOT NULL,
            total_tolls REAL NOT NULL,
            FOREIGN KEY (car_id) REFERENCES Taxi (id),
            FOREIGN KEY (driver_id) REFERENCES Driver (id)
        )
    ''')

    # Create the Job table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Job (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            driver_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            accepted TIME NOT NULL,
            meter_on TIME NOT NULL,
            meter_off TIME NOT NULL,
            pick_up_suburb TEXT NOT NULL,
            destination_suburb TEXT NOT NULL,
            fare REAL NOT NULL,
            toll REAL NOT NULL,
            account TEXT,
            taxi_id INTEGER NOT NULL,
            shift_id INTEGER NOT NULL,
            FOREIGN KEY (driver_id) REFERENCES Driver (id),
            FOREIGN KEY (taxi_id) REFERENCES Taxi (id),
            FOREIGN KEY (shift_id) REFERENCES Shift (id)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' initialized with required tables.")

def initialize_gps_database(db_name: str = 'gps_jobs.db'):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = connect(db_name)
    cursor = conn.cursor()

    # Create the GpsRecord table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS GpsRecord (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            kml_file TEXT
        )
    ''')

    # Create the ProcessedEvent table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProcessedEvent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gps_record_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            from_time TIME NOT NULL,
            to_time TIME NOT NULL,
            duration INTEGER NOT NULL,
            FOREIGN KEY (gps_record_id) REFERENCES GpsRecord (id)
        )
    ''')

    # Create the TrackerEntry table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TrackerEntry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gps_record_id INTEGER NOT NULL,
            timestamp TIME NOT NULL,
            distance REAL NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            direction TEXT,
            speed REAL,
            stop_time INTEGER,
            FOREIGN KEY (gps_record_id) REFERENCES GpsRecord (id)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' initialized with required tables.")

