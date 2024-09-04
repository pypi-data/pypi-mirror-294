from selenium import webdriver
import taxi_data_core.nextechgps_com.actions as WebSite
import taxi_data_core.nextechgps_com.schema as Schema
from datetime import datetime, time
from typing import List, Dict, Generator
from argparse import ArgumentParser
from os import getenv
from pathlib import Path
from taxi_data_core.database.initialize import initialize_gps_database
from datetime import timedelta
from re import findall
from taxi_data_core.database.actions import add_or_update_gps_records as save_data
from taxi_data_core.database.actions import fetch_all_gps_records
import xml.etree.ElementTree as ET
from taxi_data_core.nextechgps_com import constants as Constants

def initialize_browser() -> webdriver:
    browser = WebSite.login()
    browser.switch_to.default_content()
    WebSite.switch_to_main_box_iframe(browser)
    tracker = WebSite.click_on_tracker(browser)
    return browser, tracker

def date_range_generator(start_date: str, finish_date: str, date_format: str = "%d/%m/%Y") -> Generator[datetime.date, None, None]:
    """
    Generates a list of dates from start_date to finish_date using the typing.Generator type hint.

    Args:
        start_date (str): The start date in the format `date_format`.
        finish_date (str): The end date in the format `date_format`.
        date_format (str): The format of the date strings. Default is '%d/%m/%Y'.

    Yields:
        datetime.date: Each date from start_date to finish_date.
    """
    # Convert string dates to datetime.date objects
    start = datetime.strptime(start_date, date_format).date()
    end = datetime.strptime(finish_date, date_format).date()
    
    # Generate dates from start to finish
    current_date = start
    while current_date <= end:
        yield current_date
        current_date += timedelta(days=1)

def timestamp_from_string(string: str) -> time:
    hour: int= int(string.partition(" ")[2].partition(":")[0])
    minute: int = int(string.partition(" ")[2].partition(":")[2].partition(":")[0])
    second: int = int(string.partition(" ")[2].partition(":")[2].partition(":")[2])
    return time(hour, minute, second)

def safe_extract(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except (IndexError, ValueError):
        return None

def convert_to_seconds(time_str):
    # Initialize total seconds
    total_seconds = 0

    # Regular expression to find "number + unit" patterns
    matches = findall(r'(\d+)(Hour|Minute)', time_str)

    for value, unit in matches:
        value = int(value)  # Convert the value to an integer
        
        if unit == 'Hour':
            total_seconds += value * 3600  # Convert hours to seconds
        elif unit == 'Minute':
            total_seconds += value * 60  # Convert minutes to seconds

    return total_seconds

def extract_data_from_string(string: str) -> Schema.TrackerEntry:
    lines = string.splitlines()[1:]

    data_point: Schema.TrackerEntry =  Schema.TrackerEntry(
        timestamp = safe_extract(timestamp_from_string, lines[0]),
        distance = safe_extract(lambda: float(lines[1].partition(":")[2].replace("km", ""))),
        latitude = safe_extract(lambda: float(lines[2].partition(":")[2].partition(",")[0])),
        longitude = safe_extract(lambda: float(lines[2].rsplit(":")[2])))
     
    if lines[4].startswith("Stop time:"):
        data_point.stop_time = convert_to_seconds(lines[4])
    else:
        direction: str = safe_extract(lambda: lines[4].split(":")[1].split(",")[0])
        data_point.direction = direction
        data_point.speed = safe_extract(lambda: float(lines[4].split(":")[2].replace("km/h", '')))

    return data_point

def parse_raw_gps_data(raw_data: List[str]) -> List[Schema.TrackerEntry]:
    gps_data: List[Schema.TrackerEntry] = []

    for _ in raw_data:
        gps_data.append(extract_data_from_string(_))

    return gps_data

def process_raw_events(raw_events: Schema.RawEvent) -> List[Schema.ProcessedEvent]:
    
    processed_events: List[Schema.ProcessedEvent] = []

    for raw_event in raw_events:
        match raw_event.event_type:
            case "Stay": 
                event_type: Schema.GpsTrackerEvent = Schema.GpsTrackerEvent.STAY  

        from_time: time = datetime.time(datetime.strptime(raw_event.from_time, Constants.DATE_TIME_Y_M_D_H_M_S))
        to_time: time = datetime.time(datetime.strptime(raw_event.to_time, Constants.DATE_TIME_Y_M_D_H_M_S))

        processed_events.append(Schema.ProcessedEvent(event_type=event_type,
                                         from_time=from_time,
                                         to_time=to_time,
                                         duration=convert_to_seconds(raw_event.duration)))

    return processed_events

def has_coordinates_in_kml(kml_file_path: str) -> bool:
    """
    Checks if a KML file contains any coordinates.
    
    Args:
        kml_file_path (str): The path to the KML file to be checked.
    
    Returns:
        bool: True if coordinates are found, False otherwise.
    """
    try:
        tree = ET.parse(kml_file_path)
        root = tree.getroot()

        # KML files often use the 'http://www.opengis.net/kml/2.2' namespace
        ns = {'kml': 'http://www.opengis.net/kml/2.2'}

        # Find all 'coordinates' elements in the KML
        coordinates_elements = root.findall('.//kml:coordinates', ns)

        for coordinates in coordinates_elements:
            # Split by space to check if there are valid coordinate sets (longitude,latitude[,altitude])
            if coordinates.text and any(coord.strip() for coord in coordinates.text.strip().split()):
                return True

        return False
    except ET.ParseError as e:
        print(f"Error parsing KML file: {e}")
        return False
    except FileNotFoundError:
        print(f"KML file not found: {kml_file_path}")
        return False

def gather_gps_data(start_date: str, finish_date: str, destination: str) -> None:
    db_path: str = f"{destination}/gps_data.db"

    if not Path(db_path).exists():
        initialize_gps_database(db_path)
    #else:
    db_records: Dict[str, Schema.GpsRecord] = {record.date: record for record in fetch_all_gps_records(db_path)}
        

    try:
        browser, tracker = initialize_browser()        
        WebSite.nav_to_tracking_report(browser, tracker)
 
        gps_records: Dict[datetime.date, Schema.GpsRecord] = {}

        for date in date_range_generator(start_date, finish_date):
            new_record: Schema.GpsRecord = Schema.GpsRecord(date = date)
            new_record.kml_file = WebSite.set_tracking_report_date_and_go(browser, date = datetime.strftime(date, Constants.DATE_TIME_YEAR_FIRST), destination = destination)
            gps_records[date] = new_record


        browser.switch_to.default_content()

        WebSite.open_playback(browser, tracker)
        playback_buttons: Schema.PlaybackButtons = WebSite.get_playback_buttons(browser)
        WebSite.set_plaback_speed(browser, speed=Schema.PlaybackSpeed.SLOW)

        for date in date_range_generator(start_date= start_date, finish_date= finish_date):

            if gps_records[date].kml_file is None:
                kml_file_path = f"{destination}/{Constants.FILE_NAME_STRING}{datetime.strftime(date, Constants.DATE_TIME_YEAR_FIRST)}.kml"
            else:
                kml_file_path = gps_records[date].kml_file

            if has_coordinates_in_kml(kml_file_path):

                if date not in db_records:
                    WebSite.set_playback_date(browser, date)

                    raw_data: List[str] = WebSite.get_raw_data(browser, playback_buttons)
                    gps_records.get(date).gps_data = parse_raw_gps_data(raw_data)

                    raw_events: List[Schema.RawEvent] = WebSite.get_raw_events(browser)
                    gps_records.get(date).events = process_raw_events(raw_events)

    finally:
        browser.quit()

    gps_records: List[Schema.GpsRecord] = list(gps_records.values())
    save_data(gps_records, db_path)

def main() -> None:

    finish_date: datetime = datetime.now() - timedelta(days=1)
    start_date: datetime = finish_date - timedelta(days=7)

    parser = ArgumentParser(description='Gathers data from GPS tracker web portal and stores in database')
    parser.add_argument('--start_date',type=str,required=False,help="start date to get shifts and jobs from",default=start_date.strftime("%d/%m/%Y"))
    parser.add_argument('--finish_date',type=str,required=False,help="finish date to get shifts and jobs from",default=finish_date.strftime("%d/%m/%Y"))
    parser.add_argument('--destination',type=str,required=False,help="destination folder for downloaded data",default=f"{getenv('HOME')}/taxi_data")
    args, unknown = parser.parse_known_args()

    gather_gps_data(args.start_date, args.finish_date, args.destination)

if __name__ == '__main__':
    main()