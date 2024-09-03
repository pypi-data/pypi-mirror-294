from argparse import ArgumentParser
from os import getenv
from asyncio import to_thread, gather, run
from gather_taxi_data.gather_bwc_data import gather_bwc_data
from gather_taxi_data.gather_gps_data import gather_gps_data
from datetime import datetime, timedelta

async def async_gather_bwc_data(start_date: str, finish_date: str, destination: str) -> None:
    await to_thread(gather_bwc_data, start_date, finish_date, destination)

async def async_gather_gps_data(start_date: str, finish_date: str, destination: str) -> None:
    await to_thread(gather_gps_data, start_date, finish_date, destination)

async def gather_all_data(start_date: str, finish_date: str, destination: str) -> None:
    await gather(async_gather_bwc_data(start_date, finish_date, destination),
                 async_gather_gps_data(start_date, finish_date, destination))

def main() -> None:

    finish_date: datetime = datetime.now() - timedelta(days=1)
    start_date: datetime = finish_date - timedelta(days=7)

    parser = ArgumentParser(description='Gathers data all sources and stores in database')
    parser.add_argument('--start_date',type=str,required=False,help="start date to get shifts and jobs from",default=start_date.strftime("%d/%m/%Y"))
    parser.add_argument('--finish_date',type=str,required=False,help="finish date to get shifts and jobs from",default=finish_date.strftime("%d/%m/%Y"))
    parser.add_argument('--destination',type=str,required=False,help="destination folder for downloaded data",default=f"{getenv('HOME')}/taxi_data")
    args, unknown = parser.parse_known_args()

    run(gather_all_data(args.start_date, args.finish_date, args.destination))

if __name__ == '__main__':
    main()