import argparse
import pandas as pd
import json
import sys
import datetime

def calculate_mttr(json_data, start_date, end_date):
     # Filter the data based on the start and end date
    dates = json_data['Date Started']
    total_durations = json_data['Total Duration']
    report_type = json_data['Report Type']
    idxs_durations = []

    earliest_latest_dates = []
    # Loop through the dates and find the earliest date.
    if start_date is None:
        for date in dates:
            earliest_latest_dates.append(datetime.datetime.strptime(dates[date], "%m/%d/%Y"))
        start_date = min(earliest_latest_dates)
    if end_date is None:
        end_date = max(earliest_latest_dates)
    print(start_date, end_date)

    # Iterate through the dates
    for date in dates:        
        # If the date is in the range, include it to the list
        if datetime.datetime.strptime(dates[date], "%m/%d/%Y") >= start_date and datetime.datetime.strptime(dates[date], "%m/%d/%Y") <= end_date:
            timesplit = total_durations[date].split(":")
            total_minutes = int(int(timesplit[0]) * 60 + int(timesplit[1]))

            # If the total duration is less than 48 hours, include it to the list
            if total_minutes <= 2880:
                idxs_durations.append(total_minutes)
            else:
                print("Total duration is greater than 48 hours", dates[date])
        else:
            print("Date is not in the range", dates[date])
    print(idxs_durations)
    return int(sum(idxs_durations)/len(idxs_durations))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=f"python {sys.argv[0]}",
        description="This script is used to calculate the MTTR from the total duration from a CSV file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
        epilog="""
Examples:
  This will calculate the MTTR from the total duration from the CSV file from the earliest recorder report to the latest recorder report
    python main.py "<file_path>.csv"

  This will calculate the MTTR from the total duration from the CSV file from the start date specified to the latest recorder report
    python main.py "<file_path>.csv" --start-date 01/01/2025 

        This will calculate the MTTR from the total duration from the CSV file from the earliest recorder report to end date specified
        python {sys.argv[0]} "<file_path>.csv" --end-date 01/02/2025 
        
        This will calculate the MTTR from the total duration from the CSV file from the start date specified to the end date specified
        python {sys.argv[0]} "<file_path>.csv" --start-date 01/01/2025 --end-date 01/02/2025 

        """
            )
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
    parser.add_argument("filepath", type=str, help="The file path to read the data from")
    parser.add_argument("--start-date", type=str, required=False, help="The start date to calculate the MTTR from date format accepted: mm/dd/yyyy")
    parser.add_argument("--end-date", type=str, required=False, help="The end date to calculate the MTTR to date format accepted: mm/dd/yyyy")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()

    # Get the start and end date from the arguments
    start_date = args.start_date
    end_date = args.end_date
    
    # If start and end date are provided, convert them to datetime objects
    if start_date and end_date:
        start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")
    elif start_date:
        start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.datetime.now()
    elif end_date:
        end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")
        start_date = None
    else:
        start_date = None
        end_date = None

    json_data = json.loads(pd.read_csv(args.filepath).to_json())
    print(calculate_mttr(json_data, start_date, end_date))
