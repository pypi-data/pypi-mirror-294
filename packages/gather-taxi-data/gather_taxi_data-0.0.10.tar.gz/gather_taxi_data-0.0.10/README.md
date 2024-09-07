# gather_taxi_data

Gather all taxi data and store it.

## Overview

The `gather_taxi_data` package is designed to gather data from various sources such as GPS trackers and web portals, and store the collected data in a database. This package includes modules for gathering data from specific sources and a main module to orchestrate the data gathering process.

## Modules

### gather_all_data

This module gathers data from all sources and stores it in the database.

#### Functions

- `async_gather_bwc_data(start_date: str, finish_date: str, destination: str) -> None`
  - Asynchronously gathers data from the Black and White Cabs web portal.

- `async_gather_gps_data(start_date: str, finish_date: str, destination: str) -> None`
  - Asynchronously gathers data from the GPS tracker web portal.

- `gather_all_data(start_date: str, finish_date: str, destination: str) -> None`
  - Asynchronously gathers data from all sources and stores it in the database.

- `main() -> None`
  - Entry point for the module. Parses command-line arguments and initiates the data gathering process.

#### Example Usage

```sh
python -m gather_taxi_data.gather_all_data --start_date 01/01/2023 --finish_date 07/01/2023 --destination /path/to/destination
```
This command will gather all taxi data from the specified start date to the finish date and store it in the specified destination directory.

### Command-Line Arguments

- `--start_date`: The start date for data gathering in `DD/MM/YYYY` format.
- `--finish_date`: The finish date for data gathering in `DD/MM/YYYY` format.
- `--destination`: The directory where the gathered data will be stored.

### Example

To gather data from January 1, 2023, to January 7, 2023, and store it in the `/data/taxi` directory, use the following command:

```sh
python -m gather_taxi_data.gather_all_data --start_date 01/01/2023 --finish_date 07/01/2023 --destination /data/taxi
```
Make sure to replace `/data/taxi` with the actual path where you want to store the data.

### gather_bwc_data

This module gathers data specifically from the Black and White Cabs web portal.

#### Functions

- `get_driver_list(browser: webdriver) -> List[Driver]`
  - Retrieves a list of drivers from the web portal.

- `get_vehicle_list(browser: webdriver) -> List[Taxi]`
  - Retrieves a list of vehicles from the web portal.

- `duration_to_seconds(duration: str) -> int`
  - Converts a duration string to seconds.

- `get_shift_list(browser: webdriver, db_name: str, from_date: str, to_date: str) -> List[Shift]`
  - Retrieves a list of shifts from the web portal.

- `get_job_list(browser: webdriver, db_name: str) -> List[Job]`
  - Retrieves a list of jobs from the web portal.

- `gather_bwc_data(start_date: str, finish_date: str, destination: str) -> None`
  - Gathers data from the Black and White Cabs web portal and stores it in the database.

- `main() -> None`
  - Entry point for the module. Parses command-line arguments and initiates the data gathering process.

#### Example Usage

```sh
python -m gather_taxi_data.gather_bwc_data --start_date 01/01/2023 --finish_date 07/01/2023 --destination /path/to/destination
```

