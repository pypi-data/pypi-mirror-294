from selenium import webdriver
from taxi_data_core.blackandwhitecabs_com_au import constants as BwcConstants
from taxi_data_core.common import constants as CommonConstants
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import taxi_data_core.blackandwhitecabs_com_au.actions as WebSite
from taxi_data_core.blackandwhitecabs_com_au.schema import Driver, Taxi, Shift, Job
from datetime import datetime, timedelta
from typing import List, Dict
from bs4 import BeautifulSoup
from taxi_data_core.database import actions as DB
from argparse import ArgumentParser
from os import getenv
from pathlib import Path
from taxi_data_core.database.initialize import initialize_bwc_database
from taxi_data_core.common import actions as CommonActions

def get_driver_list(browser: webdriver) -> List[Driver]:
    
    WebSite.use_nav_menu(browser, link_text=BwcConstants.LINK_TEXT_DRIVERS_FOR_OPERATOR)
    WebSite.select_operator_from_drop_down(browser)

    driver_list = []

    table_rows = browser.find_elements(By.XPATH, BwcConstants.XPATH_DRIVER_ROW)
    for i in range(0, len(table_rows)):
        
        table_rows[i].find_element(By.TAG_NAME, CommonConstants.TAG_ANCHOR).click()

        WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, BwcConstants.ID_DRIVER_DETAILS)))

        # Extract the data
        soup = BeautifulSoup(browser.page_source, CommonConstants.SOUP_HTML_PARSER)
        driver_table = soup.find(CommonConstants.TAG_TABLE)

        table_dict: Dict = {}

        for row in driver_table.find_all(CommonConstants.TAG_ROW):  # Skip header  & Footer row
            
            cols = row.find_all(CommonConstants.TAG_COLUMN)

            key = cols[0].text.strip().replace(":","")
            value = cols[1].text.strip()

            table_dict[key] = value

        driver = Driver(number = table_dict[BwcConstants.DRIVER_DETAILS_NUMBER],
                        name = table_dict[BwcConstants.DRIVER_DETAILS_NAME],
                        greeting = table_dict[BwcConstants.DRIVER_DETAILS_GREETING],
                        address = table_dict[BwcConstants.DRIVER_DETAILS_ADDRESS],
                        suburb = table_dict[BwcConstants.DRIVER_DETAILS_SUBURB],
                        post_code = table_dict[BwcConstants.DRIVER_DETAILS_POST_CODE],
                        dob = datetime.strptime(table_dict[BwcConstants.DRIVER_DETAILS_DOB], CommonConstants.DEFAULT_DATE_FORMAT),
                        mobile = table_dict[BwcConstants.DRIVER_DETAILS_MOBILE],
                        city = table_dict[BwcConstants.DRIVER_DETAILS_CITY],
                        da_expiry = datetime.strptime(table_dict[BwcConstants.DRIVER_DETAILS_DA_EXPIRY], CommonConstants.DEFAULT_DATE_FORMAT),
                        license_expiry = datetime.strptime(table_dict[BwcConstants.DRIVER_DETAILS_LICENSE_EXPIRY], CommonConstants.DEFAULT_DATE_FORMAT),
                        conditions = table_dict[BwcConstants.DRIVER_DETAILS_CONDITIONS],
                        create_date = datetime.strptime(table_dict[BwcConstants.DRIVER_DETAILS_CREATED], CommonConstants.DEFAULT_DATE_FORMAT),
                        first_logon = datetime.strptime(table_dict[BwcConstants.DRIVER_DETAILS_FIRST_LOGON], CommonConstants.DEFAULT_DATE_FORMAT),
                        last_logon = datetime.strptime(table_dict[BwcConstants.DRIVER_DETAILS_LAST_LOGON], CommonConstants.DEFAULT_DATE_FORMAT),
                        first_operator_logon = datetime.strptime(table_dict[BwcConstants.DRIVER_DETAILS_FIRST_OPERATOR_LOGON], CommonConstants.DEFAULT_DATE_FORMAT),
                        logons_for_operator = table_dict[BwcConstants.DRIVER_DETAILS_LOGON_LAST_180],
                        hours_for_operator = table_dict[BwcConstants.DRIVER_DETAILS_HOURS_LAST_180])
        
        driver_list.append(driver)
        
    return driver_list

def get_vehicle_list(browser: webdriver) -> List[Taxi]:
    
    WebSite.use_nav_menu(browser, link_text=BwcConstants.LINK_TEXT_VEHICLES_FOR_OPERATOR)
    WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, BwcConstants.ID_VEHICLES_LIST)))
    vehicle_list: List[Taxi] = []

    soup = BeautifulSoup(browser.page_source, CommonConstants.SOUP_HTML_PARSER)
    car_table = soup.find(CommonConstants.TAG_TABLE, {CommonConstants.TAG_ID: BwcConstants.ID_VEHICLES_LIST})

    for row in car_table.find_all(CommonConstants.TAG_ROW)[CommonConstants.SLICE_REMOVE_HEADER]:
        cols = row.find_all(CommonConstants.TAG_COLUMN)

        taxi: Taxi = Taxi(number = cols[0].text.strip(),
                          primary_fleet = cols[1].text.strip(),
                          rego = cols[2].text.strip(),
                          rego_expiry = datetime.strptime(cols[3].text.strip(), CommonConstants.DEFAULT_DATE_FORMAT),
                          coi_expiry = datetime.strptime(cols[4].text.strip(), CommonConstants.DEFAULT_DATE_FORMAT),
                          fleets = cols[5].text.strip(),
                          conditions = cols[6].text.strip(),
                          make = cols[7].text.strip(),
                          model = cols[8].text.strip(),
                          build_date = cols[9].text.strip(),
                          pax = cols[10].text.strip())
        vehicle_list.append(taxi)

    return vehicle_list

def duration_to_seconds(duration: str) -> int:
    parts = duration.split(":")
    
    # Assume if the input has two parts, it's "HH:MM" format
    if len(parts) == 2:
        hours, minutes = map(int, parts)
        seconds = hours * 3600 + minutes * 60  # Convert to seconds
    else:
        raise ValueError("Input string format is not supported.")
    
    return seconds

def get_shift_list(browser: webdriver, db_name: str, from_date: str, to_date: str) -> List[Shift]:

    # Iterate over each shift and extract job data
    shift_list = []
    car_rows = browser.find_elements(By.XPATH, BwcConstants.XPATH_VEHICLE_ROW)

    for i in range(0, len(car_rows)):
        car_rows[i].find_element(By.TAG_NAME, CommonConstants.TAG_ANCHOR).click()

        WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, BwcConstants.ID_SHIFTS_FOR_VEHICLE)))
        WebSite.shifts_for_vehicle_set_date_range(browser, datetime.strptime(from_date, CommonConstants.DEFAULT_DATE_FORMAT), datetime.strptime(to_date, CommonConstants.DEFAULT_DATE_FORMAT))
        
        soup = BeautifulSoup(browser.page_source, CommonConstants.SOUP_HTML_PARSER)
        shifts_table = soup.find(CommonConstants.TAG_TABLE, {CommonConstants.TAG_ID: BwcConstants.ID_SHIFTS_FOR_VEHICLE})

        for row in shifts_table.find_all(CommonConstants.TAG_ROW)[CommonConstants.SLICE_REMOVE_HEADER_FOOTER]:  # Skip header  & Footer row
            cols = row.find_all(CommonConstants.TAG_COLUMN)

            shift = Shift(car_id = DB.get_taxi_id_by_number(cols[0].text.strip(), db_name),
                          driver_id = DB.get_driver_id_by_number(cols[1].text.split(), db_name),
                          name = cols[2].text.strip(),
                          log_on = datetime.strptime(cols[3].text.strip(), CommonConstants.DEFAULT_DATE_TIME_FORMAT),
                          log_off = datetime.strptime(cols[4].text.strip(), CommonConstants.DEFAULT_DATE_TIME_FORMAT),
                          duration = duration_to_seconds(cols[5].text.strip()),
                          distance = cols[6].text.strip(),
                          offered = cols[7].text.strip(),
                          accepted = cols[8].text.strip(),
                          rejected = cols[9].text.strip(),
                          recalled = cols[10].text.strip(),
                          completed = cols[11].text.strip(),
                          total_fares = CommonActions.string_to_float(cols[12].text.strip()),
                          total_tolls = CommonActions.string_to_float(cols[13].text.strip()))
            shift_list.append(shift)

        # Go back to the shift list page to process the next shift
        browser.back()
        WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, BwcConstants.ID_SHIFTS_FOR_VEHICLE)))
        car_rows = browser.find_elements(By.XPATH, BwcConstants.XPATH_VEHICLE_ROW)
    
    return shift_list

def get_job_list(browser: webdriver, db_name: str) -> List[Job]:
    # Iterate over each shift and extract job data
    jobs_data = []
    shift_rows = browser.find_elements(By.XPATH, BwcConstants.XPATH_SHIFT_ROW)

    for i in range(0, len(shift_rows)):
        # Click on the browser ID link for each shift
        car_number: str = shift_rows[i].text.split(" ")[0]
        shift_logon: datetime = datetime.strptime(f'{shift_rows[i].text.split(" ")[5]} {shift_rows[i].text.split(" ")[6]}', "%d/%m/%Y %H:%M")
        shift_rows[i].find_element(By.TAG_NAME, CommonConstants.TAG_ANCHOR).click()
        
        # Wait for job list to load
        WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, BwcConstants.ID_JOBS_FOR_SHIFT)))

        # Extract the job data
        soup = BeautifulSoup(browser.page_source, CommonConstants.SOUP_HTML_PARSER)
        jobs_table = soup.find(CommonConstants.TAG_TABLE, {CommonConstants.TAG_ID: BwcConstants.ID_JOBS_FOR_SHIFT})

        for row in jobs_table.find_all(CommonConstants.TAG_ROW)[CommonConstants.SLICE_REMOVE_HEADER_FOOTER]:  # Skip header  & Footer row
            cols = row.find_all(CommonConstants.TAG_COLUMN)
            job = Job(booking_id=int(cols[0].text.strip()),
                    driver_id = DB.get_driver_id_by_number(cols[1].text.split(), db_name),
                    status=cols[2].text.strip(),
                    accepted=cols[3].text.strip(),
                    meter_on=cols[4].text.strip(),
                    meter_off=cols[5].text.strip(),
                    pick_up_suburb=cols[6].text.strip(),
                    destination_suburb=cols[7].text.strip(),
                    fare=CommonActions.string_to_float(cols[8].text.strip()),
                    toll=CommonActions.string_to_float(cols[9].text.strip()),
                    account=cols[10].text.strip(),
                    taxi_id = DB.get_taxi_id_by_number(car_number, db_name),
                    shift_id = DB.get_shift_id_by_logon(db_name = db_name, logon = shift_logon))
            jobs_data.append(job)

        # Go back to the shift list page to process the next shift
        browser.back()
        WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, BwcConstants.ID_SHIFTS_FOR_VEHICLE)))
        shift_rows = browser.find_elements(By.XPATH, BwcConstants.XPATH_SHIFT_ROW)
    return jobs_data

def gather_bwc_data(start_date: str, finish_date: str, destination: str) -> None:
    db_path: str = f"{destination}/bwc_data.db"

    if not Path(db_path).exists():
        initialize_bwc_database(db_path)

    try:
        browser: webdriver = WebSite.initialize_browser()

        driver_list: List[Driver] = get_driver_list(browser)
        DB.update_driver_list(drivers = driver_list, db_name = db_path)

        vehicle_list: List[Taxi] = get_vehicle_list(browser) 
        DB.update_taxi_list(taxis = vehicle_list, db_name = db_path)

        shift_list: List[Shift] = get_shift_list(browser, db_name = db_path, from_date = start_date, to_date = finish_date)
        DB.update_shift_list(shifts = shift_list, db_name = db_path)

        job_list: List[Job] = get_job_list(browser, db_name = db_path)
        DB.add_jobs_to_database(jobs = job_list, db_name = db_path)

    except Exception as e:
        raise e
    finally:
        browser.quit()

def main() -> None:

    finish_date: datetime = datetime.now() - timedelta(days=1)
    start_date: datetime = finish_date - timedelta(days=7)

    parser = ArgumentParser(description='Gathers data from BWWC web portal and stores in database')
    parser.add_argument('--start_date',type=str,required=False,help="start date to get shifts and jobs from",default=start_date.strftime(CommonConstants.DEFAULT_DATE_FORMAT))
    parser.add_argument('--finish_date',type=str,required=False,help="finish date to get shifts and jobs from",default=finish_date.strftime(CommonConstants.DEFAULT_DATE_FORMAT))
    parser.add_argument('--destination',type=str,required=False,help="destination folder for downloaded data",default=f"{getenv('HOME')}/taxi_data")
    args, unknown = parser.parse_known_args()

    gather_bwc_data(args.start_date, args.finish_date, args.destination)

if __name__ == '__main__':
    main()