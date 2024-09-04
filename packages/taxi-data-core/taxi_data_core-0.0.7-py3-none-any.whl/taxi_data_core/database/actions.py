from typing import List, Optional
from taxi_data_core.blackandwhitecabs_com_au.schema import Driver, Taxi, Shift, Job
from taxi_data_core.nextechgps_com.schema import GpsRecord, ProcessedEvent, GpsTrackerEvent, TrackerEntry
from sqlite3 import connect
from argparse import ArgumentParser
from os import getenv
from pathlib import Path
from datetime import datetime
from taxi_data_core.database import constants as Constants

def update_driver_list(drivers: List[Driver], db_name: str = 'gps_jobs.db'):
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()

    # SQL query to check if a driver exists
    check_driver_query = "SELECT id FROM Driver WHERE number = ?"

    # SQL query to insert a new driver
    insert_driver_query = '''
    INSERT INTO Driver (
        number, name, greeting, address, suburb, post_code, dob, mobile, city, da_expiry,
        license_expiry, auth_wheelchair, auth_bc, auth_redcliffe, auth_london, auth_mandurah,
        refer_fleet_ops, conditions, create_date, first_logon, last_logon, first_operator_logon,
        logons_for_operator, hours_for_operator, validation_active, validation_until, validation_reason
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # SQL query to update an existing driver
    update_driver_query = '''
    UPDATE Driver SET
        name = ?, greeting = ?, address = ?, suburb = ?, post_code = ?, dob = ?, mobile = ?, city = ?,
        da_expiry = ?, license_expiry = ?, auth_wheelchair = ?, auth_bc = ?, auth_redcliffe = ?, auth_london = ?,
        auth_mandurah = ?, refer_fleet_ops = ?, conditions = ?, create_date = ?, first_logon = ?, last_logon = ?,
        first_operator_logon = ?, logons_for_operator = ?, hours_for_operator = ?, validation_active = ?,
        validation_until = ?, validation_reason = ?
    WHERE number = ?
    '''

    # Iterate through the list of drivers
    for driver in drivers:
        # Check if the driver already exists in the database
        cursor.execute(check_driver_query, (driver.number,))
        result = cursor.fetchone()

        # If driver exists, update the details
        if result:
            cursor.execute(update_driver_query, (
                driver.name, driver.greeting, driver.address, driver.suburb, driver.post_code, driver.dob, 
                driver.mobile, driver.city, driver.da_expiry, driver.license_expiry, driver.auth_wheelchair, 
                driver.auth_bc, driver.auth_redcliffe, driver.auth_london, driver.auth_mandurah, 
                driver.refer_fleet_ops, driver.conditions, driver.create_date, driver.first_logon, driver.last_logon, 
                driver.first_operator_logon, driver.logons_for_operator, driver.hours_for_operator, 
                driver.validation_active, driver.validation_until, driver.validation_reason, driver.number
            ))
        # If driver does not exist, insert a new record
        else:
            cursor.execute(insert_driver_query, (
                driver.number, driver.name, driver.greeting, driver.address, driver.suburb, driver.post_code, 
                driver.dob, driver.mobile, driver.city, driver.da_expiry, driver.license_expiry, 
                driver.auth_wheelchair, driver.auth_bc, driver.auth_redcliffe, driver.auth_london, 
                driver.auth_mandurah, driver.refer_fleet_ops, driver.conditions, driver.create_date, 
                driver.first_logon, driver.last_logon, driver.first_operator_logon, driver.logons_for_operator, 
                driver.hours_for_operator, driver.validation_active, driver.validation_until, driver.validation_reason
            ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Driver data has been updated in the '{db_name}' database.")

def get_drivers_from_database(db_name: str = 'gps_jobs.db') -> List[Driver]:
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()

    # Query to select all drivers from the Driver table
    cursor.execute('SELECT * FROM Driver')
    
    # Fetch all results from the query
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # List to store the Driver objects
    drivers = []

    # Column order based on the Driver table schema
    for row in rows:
        driver = Driver(
            number=row[1],  # assuming the number is in the second column (index 1)
            name=row[2],
            greeting=row[3],
            address=row[4],
            suburb=row[5],
            post_code=row[6],
            dob=datetime.strptime(row[7], Constants.DATE_FORMAT),  # convert string to datetime
            mobile=row[8],
            city=row[9],
            da_expiry=datetime.strptime(row[10], Constants.DATE_FORMAT),
            license_expiry=datetime.strptime(row[11], Constants.DATE_FORMAT),
            auth_wheelchair=row[12],
            auth_bc=row[13],
            auth_redcliffe=row[14],
            auth_london=row[15],
            auth_mandurah=row[16],
            refer_fleet_ops=row[17],
            conditions=row[18],
            create_date=datetime.strptime(row[19], Constants.DATE_FORMAT),
            first_logon=datetime.strptime(row[20], Constants.DATE_FORMAT),
            last_logon=datetime.strptime(row[21], Constants.DATE_FORMAT),
            first_operator_logon=datetime.strptime(row[22], Constants.DATE_FORMAT),
            logons_for_operator=row[23],
            hours_for_operator=row[24],
            validation_active=row[25],
            validation_until=datetime.strptime(row[26], Constants.DATE_FORMAT) if row[26] else None,
            validation_reason=row[27]
        )
        drivers.append(driver)

    # Return the list of Driver objects
    return drivers

def update_taxi_list(taxis: List[Taxi], db_name: str = 'gps_jobs.db'):
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()

    # Iterate over the list of taxis
    for taxi in taxis:
        # Check if the taxi already exists in the database using the 'number' field
        cursor.execute("SELECT id FROM Taxi WHERE number = ?", (taxi.number,))
        result = cursor.fetchone()

        if result:
            # Taxi exists, perform an update
            cursor.execute('''
                UPDATE Taxi
                SET primary_fleet = ?, rego = ?, rego_expiry = ?, coi_expiry = ?, fleets = ?, conditions = ?, 
                    make = ?, model = ?, build_date = ?, pax = ?, validation = ?, until = ?, reason = ?
                WHERE number = ?
            ''', (taxi.primary_fleet, taxi.rego, taxi.rego_expiry, taxi.coi_expiry, taxi.fleets, taxi.conditions,
                  taxi.make, taxi.model, taxi.build_date, taxi.pax, taxi.validation, taxi.until, taxi.reason, taxi.number))
        else:
            # Taxi does not exist, perform an insert
            cursor.execute('''
                INSERT INTO Taxi (number, primary_fleet, rego, rego_expiry, coi_expiry, fleets, conditions, make, model, build_date, pax, validation, until, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (taxi.number, taxi.primary_fleet, taxi.rego, taxi.rego_expiry, taxi.coi_expiry, taxi.fleets, taxi.conditions,
                  taxi.make, taxi.model, taxi.build_date, taxi.pax, taxi.validation, taxi.until, taxi.reason))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Taxi data has been updated in the '{db_name}' database.")

def get_taxis_from_database(db_name: str = 'gps_jobs.db') -> List[Taxi]:
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()

    # Retrieve all records from the Taxi table
    cursor.execute('SELECT number, primary_fleet, rego, rego_expiry, coi_expiry, fleets, conditions, make, model, build_date, pax, validation, until, reason FROM Taxi')
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert rows to a list of Taxi objects
    taxis = [
        Taxi(
            number=row[0],
            primary_fleet=row[1],
            rego=row[2],
            rego_expiry=row[3],
            coi_expiry=row[4],
            fleets=row[5],
            conditions=row[6],
            make=row[7],
            model=row[8],
            build_date=row[9],
            pax=row[10],
            validation=row[11],
            until=row[12],
            reason=row[13]
        )
        for row in rows
    ]

    return taxis

def update_shift_list(shifts: List[Shift], db_name: str = 'gps_jobs.db'):
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()

    for shift in shifts:

        cursor.execute('SELECT number FROM Driver WHERE id = ?', (shift.driver_id,))
        driver_number: int = cursor.fetchone()[0]

        cursor.execute('SELECT number FROM Taxi WHERE id = ?', (shift.car_id,))
        car_number: str = cursor.fetchone()[0]


        # Check if the shift already exists based on the log_on field
        cursor.execute('''
            SELECT COUNT(*) FROM Shift WHERE log_on = ?
        ''', (shift.log_on,))
        exists = cursor.fetchone()[0]

        if exists:
            print(f"Shift for car {car_number} with driver {driver_number} on {shift.log_on} already exists. Skipping insertion.")
            continue

        # Insert the shift record
        cursor.execute('''
            INSERT INTO Shift (car_id, driver_id, name, log_on, log_off, duration, distance, offered, accepted, rejected, recalled, completed, total_fares, total_tolls)
            VALUES ((SELECT id FROM Taxi WHERE id = ?), (SELECT id FROM Driver WHERE id = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (shift.car_id, shift.driver_id, shift.name, shift.log_on, shift.log_off, shift.duration, shift.distance, shift.offered, shift.accepted, shift.rejected, shift.recalled, shift.completed, shift.total_fares, shift.total_tolls))

        print(f"Inserted shift for car {car_number} with driver {driver_number} on {shift.log_on}.")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Database updated successfully with shifts.")

def get_driver_id_by_number(driver_number: int, db_name: str = 'gps_jobs.db') -> Optional[int]:
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()

    # SQL query to find the driver ID by driver number
    query = 'SELECT id FROM Driver WHERE number = ?'
    
    # Execute the query with the driver_number as parameter
    cursor.execute(query, (driver_number[0],))
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()

    # Check if a result was found and return the driver ID, else return None
    if result:
        return result[0]  # The id is the first (and only) column in the result
    else:
        return None
    
def get_taxi_id_by_number(taxi_number: str, db_name: str = 'gps_jobs.db') -> Optional[int]:
    """
    Fetches the taxi ID from the database based on the taxi number.

    :param taxi_number: The number of the taxi to search for.
    :param db_name: The name of the database file.
    :return: The ID of the taxi if found, otherwise None.
    """
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()

    # Query to find the taxi ID by number
    cursor.execute('SELECT id FROM Taxi WHERE number = ?', (taxi_number,))
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    # If a result is found, return the ID; otherwise, return None
    if result:
        return result[0]  # result[0] is the taxi ID
    else:
        return None

def get_shifts_from_database(db_name: str = 'gps_jobs.db') -> List[Shift]:
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()

    # Query to get all shifts
    cursor.execute('SELECT * FROM Shift')
    shifts = cursor.fetchall()

    shift_list = []

    # Iterate over each shift record
    for shift in shifts:
        shift_id, car_id, driver_id, name, log_on, log_off, duration, distance, offered, accepted, \
        rejected, recalled, completed, total_fares, total_tolls = shift
        
        # Query for the associated Taxi record
        cursor.execute('SELECT * FROM Taxi WHERE id = ?', (car_id,))
        taxi_record = cursor.fetchone()
        if taxi_record:
            taxi = Taxi(
                id=taxi_record[0],
                number=taxi_record[1],
                primary_fleet=taxi_record[2],
                rego=taxi_record[3],
                rego_expiry=datetime.strptime(taxi_record[4], Constants.DATE_FORMAT).date(),
                coi_expiry=datetime.strptime(taxi_record[5], Constants.DATE_FORMAT).date(),
                fleets=taxi_record[6],
                conditions=taxi_record[7],
                make=taxi_record[8],
                model=taxi_record[9],
                build_date=taxi_record[10],
                pax=taxi_record[11],
                validation=taxi_record[12],
                until=datetime.strptime(taxi_record[13], Constants.DATE_FORMAT).date() if taxi_record[13] else None,
                reason=taxi_record[14]
            )
        else:
            continue  # If the taxi record is not found, skip to the next shift

        # Query for the associated Driver record
        cursor.execute('SELECT * FROM Driver WHERE id = ?', (driver_id,))
        driver_record = cursor.fetchone()
        if driver_record:
            driver = Driver(
                id=driver_record[0],
                number=driver_record[1],
                name=driver_record[2],
                greeting=driver_record[3],
                address=driver_record[4],
                suburb=driver_record[5],
                post_code=driver_record[6],
                dob=datetime.strptime(driver_record[7], Constants.DATE_FORMAT).date(),
                mobile=driver_record[8],
                city=driver_record[9],
                da_expiry=datetime.strptime(driver_record[10], Constants.DATE_FORMAT).date(),
                license_expiry=datetime.strptime(driver_record[11], Constants.DATE_FORMAT).date(),
                auth_wheelchair=driver_record[12],
                auth_bc=driver_record[13],
                auth_redcliffe=driver_record[14],
                auth_london=driver_record[15],
                auth_mandurah=driver_record[16],
                refer_fleet_ops=driver_record[17],
                conditions=driver_record[18],
                create_date=datetime.strptime(driver_record[19], Constants.DATE_FORMAT).date(),
                first_logon=datetime.strptime(driver_record[20], Constants.DATE_FORMAT).date(),
                last_logon=datetime.strptime(driver_record[21], Constants.DATE_FORMAT).date(),
                first_operator_logon=datetime.strptime(driver_record[22], Constants.DATE_FORMAT).date(),
                logons_for_operator=driver_record[23],
                hours_for_operator=driver_record[24],
                validation_active=driver_record[25],
                validation_until=datetime.strptime(driver_record[26], Constants.DATE_FORMAT).date() if driver_record[26] else None,
                validation_reason=driver_record[27]
            )
        else:
            continue  # If the driver record is not found, skip to the next shift

        # Create Shift object with Taxi and Driver objects
        shift_obj = Shift(
            car_id=taxi,
            driver_id=driver,
            name=name,
            log_on=datetime.strptime(log_on, '%Y-%m-%d %H:%M:%S'),
            log_off=datetime.strptime(log_off, '%Y-%m-%d %H:%M:%S'),
            duration=duration,
            distance=distance,
            offered=offered,
            accepted=accepted,
            rejected=rejected,
            recalled=recalled,
            completed=completed,
            total_fares=total_fares,
            total_tolls=total_tolls
        )

        # Append to the list of shifts
        shift_list.append(shift_obj)

    # Close the database connection
    conn.close()

    return shift_list

def get_shift_id_by_logon(logon: datetime, db_name: str = 'gps_jobs.db') -> int:
    """
    Fetches the shift ID from the database based on the logon date and time.

    :param logon: datetime to search for.
    :param db_name: The name of the database file.
    :return: The ID of the shift if found, otherwise None.
    """
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()
    logon_string: str = datetime.strftime(logon, "%d/%m/%Y %H:%M")

    # Query to find the taxi ID by number
    cursor.execute('SELECT id FROM Shift WHERE log_on = ?', (logon,))
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    # If a result is found, return the ID; otherwise, return None
    if result:
        return result[0]  # result[0] is the taxi ID
    else:
        return None

def add_jobs_to_database(jobs: List[Job], db_name: str = 'gps_jobs.db'):
    # Connect to the database
    conn = connect(db_name)
    cursor = conn.cursor()

    try:
        for job in jobs:
            # Check if job already exists in the database
            cursor.execute('SELECT COUNT(*) FROM Job WHERE booking_id = ?', (job.booking_id,))
            exists = cursor.fetchone()[0] > 0

            if exists:
                print(f"Job with booking_id {job.booking_id} already exists. Skipping insertion.")
                continue

            # Convert related objects to their IDs if necessary
            driver_id = job.driver_id if isinstance(job.driver_id, int) else job.driver_id.id
            taxi_id = job.taxi_id if isinstance(job.taxi_id, int) else job.taxi_id.id
            shift_id = job.shift_id if isinstance(job.shift_id, int) else job.shift_id.id

            # Insert job into the database
            cursor.execute('''
                INSERT INTO Job (
                    booking_id, driver_id, status, accepted, meter_on, meter_off,
                    pick_up_suburb, destination_suburb, fare, toll, account, taxi_id, shift_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job.booking_id,
                driver_id,
                job.status,
                job.accepted.strftime('%H:%M:%S'),
                job.meter_on.strftime('%H:%M:%S'),
                job.meter_off.strftime('%H:%M:%S'),
                job.pick_up_suburb,
                job.destination_suburb,
                job.fare,
                job.toll,
                job.account,
                taxi_id,
                shift_id
            ))

            print(f"Job with booking_id {job.booking_id} added successfully.")

        # Commit the transaction
        conn.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

def get_all_jobs_from_database(db_name: str = 'gps_jobs.db') -> List[Job]:
    # Connect to the database
    conn = connect(db_name)
    cursor = conn.cursor()

    # List to store the jobs
    jobs = []

    try:
        # Query to get all jobs
        cursor.execute('SELECT * FROM Job')
        job_rows = cursor.fetchall()

        for job_row in job_rows:
            # Extract job data from row
            (job_id, booking_id, driver_id, status, accepted, meter_on, meter_off,
             pick_up_suburb, destination_suburb, fare, toll, account, taxi_id, shift_id) = job_row

            # Fetch the driver, taxi, and shift data based on their IDs
            cursor.execute('SELECT * FROM Driver WHERE id = ?', (driver_id,))
            driver_row = cursor.fetchone()
            driver = Driver(**dict(zip([column[0] for column in cursor.description], driver_row)))

            cursor.execute('SELECT * FROM Taxi WHERE id = ?', (taxi_id,))
            taxi_row = cursor.fetchone()
            taxi = Taxi(**dict(zip([column[0] for column in cursor.description], taxi_row)))

            cursor.execute('SELECT * FROM Shift WHERE id = ?', (shift_id,))
            shift_row = cursor.fetchone()
            shift = Shift(**dict(zip([column[0] for column in cursor.description], shift_row)))

            # Convert time fields from string to datetime.time objects
            accepted_time = datetime.strptime(accepted, '%H:%M:%S').time()
            meter_on_time = datetime.strptime(meter_on, '%H:%M:%S').time()
            meter_off_time = datetime.strptime(meter_off, '%H:%M:%S').time()

            # Create a Job object and append it to the jobs list
            job = Job(
                booking_id=booking_id,
                driver_id=driver,
                status=status,
                accepted=accepted_time,
                meter_on=meter_on_time,
                meter_off=meter_off_time,
                pick_up_suburb=pick_up_suburb,
                destination_suburb=destination_suburb,
                fare=fare,
                toll=toll,
                account=account,
                taxi_id=taxi,
                shift_id=shift
            )
            jobs.append(job)
    except Exception as e:
        print(f"An error occurred while retrieving jobs: {e}")
    finally:
        # Close the database connection
        conn.close()

    return jobs

def add_or_update_gps_records(records: List[GpsRecord], db_name: str = 'gps_jobs.db'):
    # Connect to the SQLite database
    conn = connect(db_name)
    cursor = conn.cursor()

    # Iterate over each GpsRecord in the list
    for record in records:
        # Convert the date to a string format compatible with SQLite
        record_date_str = record.date.strftime(Constants.DATE_FORMAT)
        
        # Check if the GpsRecord already exists in the database based on the 'date' field
        cursor.execute('SELECT id FROM GpsRecord WHERE date = ?', (record_date_str,))
        gps_record_id = cursor.fetchone()
        
        if gps_record_id:
            # Record exists, get the ID
            gps_record_id = gps_record_id[0]
        else:
            # Insert a new GpsRecord entry
            cursor.execute(
                'INSERT INTO GpsRecord (date, kml_file) VALUES (?, ?)',
                (record_date_str, str(record.kml_file) if record.kml_file else None)
            )
            gps_record_id = cursor.lastrowid  # Get the new ID of the inserted record
        
        # Insert or update ProcessedEvent entries
        if record.events:
            for event in record.events:
                # Convert time objects to string format 'HH:MM:SS'
                from_time_str = event.from_time.strftime('%H:%M:%S')
                
                # Check if the ProcessedEvent already exists in the database
                cursor.execute('''
                    SELECT id FROM ProcessedEvent 
                    WHERE gps_record_id = ? AND from_time = ?
                ''', (gps_record_id, from_time_str))
                
                if cursor.fetchone() is None:
                    # Convert time objects to string format 'HH:MM:SS'
                    to_time_str = event.to_time.strftime('%H:%M:%S')
                    
                    # Insert a new ProcessedEvent entry
                    cursor.execute('''
                        INSERT INTO ProcessedEvent (gps_record_id, event_type, from_time, to_time, duration) 
                        VALUES (?, ?, ?, ?, ?)
                    ''', (gps_record_id, event.event_type.name, from_time_str, to_time_str, event.duration))

        # Insert or update TrackerEntry entries
        if record.gps_data:
            for entry in record.gps_data:
                # Convert time objects to string format 'HH:MM:SS'
                timestamp_str = entry.timestamp.strftime('%H:%M:%S')
                
                # Check if the TrackerEntry already exists in the database
                cursor.execute('''
                    SELECT id FROM TrackerEntry 
                    WHERE gps_record_id = ? AND timestamp = ?
                ''', (gps_record_id, timestamp_str))
                
                if cursor.fetchone() is None:
                    # Insert a new TrackerEntry entry
                    cursor.execute('''
                        INSERT INTO TrackerEntry (gps_record_id, timestamp, distance, latitude, longitude, direction, speed, stop_time) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (gps_record_id, timestamp_str, entry.distance, entry.latitude, entry.longitude, 
                          entry.direction, entry.speed, entry.stop_time))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Records have been added or updated in the '{db_name}' database.")

def fetch_all_gps_records(db_name: str = 'gps_jobs.db') -> List[GpsRecord]:
    conn = connect(db_name)
    cursor = conn.cursor()

    # Fetch all GpsRecords
    cursor.execute('SELECT id, date, kml_file FROM GpsRecord')
    gps_records = cursor.fetchall()

    records = []

    # For each GpsRecord, fetch associated ProcessedEvent and TrackerEntry
    for record_id, record_date, kml_file in gps_records:
        # Fetch ProcessedEvents associated with the GpsRecord
        cursor.execute('''
            SELECT event_type, from_time, to_time, duration 
            FROM ProcessedEvent 
            WHERE gps_record_id = ?
        ''', (record_id,))
        processed_events = cursor.fetchall()

        # Convert to ProcessedEvent objects
        events = []
        for event in processed_events:
            event_type_str = event[0]
            try:
                # Normalize case to match enum values
                event_type = GpsTrackerEvent(event_type_str.capitalize())  # Properly convert string to GpsTrackerEvent enum
            except ValueError:
                print(f"Warning: Unknown event type '{event_type_str}' found in database.")
                continue  # Skip or handle the unknown event type

            events.append(
                ProcessedEvent(
                    event_type=event_type,
                    from_time=event[1],
                    to_time=event[2],
                    duration=event[3]
                )
            )

        # Fetch TrackerEntries associated with the GpsRecord
        cursor.execute('''
            SELECT timestamp, distance, latitude, longitude, direction, speed, stop_time 
            FROM TrackerEntry 
            WHERE gps_record_id = ?
        ''', (record_id,))
        tracker_entries = cursor.fetchall()

        # Convert to TrackerEntry objects
        gps_data = [
            TrackerEntry(
                timestamp=entry[0],
                distance=entry[1],
                latitude=entry[2],
                longitude=entry[3],
                direction=entry[4],
                speed=entry[5],
                stop_time=entry[6]
            )
            for entry in tracker_entries
        ]

        # Create GpsRecord object with associated events and gps_data
        gps_record = GpsRecord(
            date=record_date,
            kml_file=Path(kml_file) if kml_file else None,
            events=events,
            gps_data=gps_data
        )

        records.append(gps_record)

    # Close the connection
    conn.close()

    return records

def main() -> None:

    parser = ArgumentParser(description='Initializes database')
    parser.add_argument('--path',type=str,required=False,help="Database file path",default=f"{getenv('HOME')}/bwc_data.db")
    parser.add_argument('--destination',type=str,required=False,help="destination folder for downloaded data",default=f"{getenv('HOME')}/taxi_data")
    args, unknown = parser.parse_known_args()

    bwc_db: Path = Path(f"{args.destination}/bwc_data.db")
    gps_db: Path = Path(f"{args.destination}/gps_data.db")

    driver_list: List[Driver] = get_drivers_from_database(bwc_db)
    taxi_list: List[Taxi] = get_taxis_from_database(bwc_db)
    shift_list: List[Shift] = get_shifts_from_database(bwc_db)
    job_list: List[Job] = get_all_jobs_from_database(bwc_db)
    gps_records: list[GpsRecord] = fetch_all_gps_records(gps_db)

    print(driver_list)
    print(taxi_list)
    print(shift_list)
    print(job_list)
    print(gps_records)

if __name__ == '__main__':
    main()