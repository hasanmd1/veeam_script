# This is a sample Python script.
import argparse
import hashlib
import os.path
import shutil
import time
import sys
from datetime import datetime, timedelta

# just used custom-function for safety
def md5_calculation(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def synchronize_folders(source_folder, replica_folder, log_file):

    source_folder = str(source_folder)
    replica_folder = str(replica_folder)

    if not os.path.exists(replica_folder):
        os.mkdir(replica_folder)

    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:
            log.write(f'{datetime.now()} - Log file created: {log_file}\n')
            print(f'{datetime.now()} - Log file created: {log_file}')

    with open(log_file, 'a') as log:
        for root, dirs, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            target_root = os.path.join(replica_folder, relative_path)
            if not os.path.exists(target_root):
                os.makedirs(target_root)
                log.write(f'{datetime.now()} - Created folder: {target_root}\n')
                print(f'{datetime.now()} - Created folder: {target_root}')

            for file in files:
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_root, file)

                if not os.path.exists(target_file) or md5_calculation(source_file) != md5_calculation(target_file):
                    shutil.copy2(source_file, target_file)
                    log.write(f'{datetime.now()} - Copied file: {source_file} to {target_file}\n')
                    print(f'{datetime.now()} - Copied file: {source_file} to {target_file}')

            # explore source_folder and remove files that dont exist
            source_root = os.path.join(source_folder, relative_path)
            for file in files:
                replica_file = os.path.join(root, file)
                source_file = os.path.join(source_root, file)

                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    log.write(f'{datetime.now()} - Removed file: {replica_file}\n')
                    print(f'{datetime.now()} - Removed file: {replica_file}')

            for directory in dirs:
                replica_dir = os.path.join(root, directory)
                source_dir = os.path.join(source_root, directory)

                if not os.path.exists(source_dir):
                    shutil.rmtree(replica_dir)
                    log.write(f'{datetime.now()} - Removed folder: {replica_dir}\n')
                    print(f'{datetime.now()} - Removed folder: {replica_dir}')


def parse_day_time(time_string):
    try:
        days, hours, minutes, seconds = map(int, time_string.split(':'))
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    except:
        raise argparse.ArgumentTypeError('Invalid time format. Use DD:HH::MM:SS (24-hour for HH format)')

# in case you forgot to pass arguments
def test_main():
    print("Enter the source folder path:")
    source_folder = input().strip()

    print("Enter the replica folder path:")
    replica_folder = input().strip()

    print("Enter the log file path:")
    log_file = input().strip()

    print("Enter the synchronization interval (format: 'X day(s) Y hour(s) Z minute(s) N second(s)'):")
    interval_str = input().strip()

    try:
        periodic_run_interval = parse_day_time(interval_str)  # This assumes you have a parser for the time format
    except Exception as e:
        print(f"Invalid interval format. Error: {e}")
        return

    try:
        print(f"Synchronization started at: {datetime.now()}")
        synchronize_folders(source_folder, replica_folder, log_file)
        print(f"Synchronization complete. Next synchronization after: {periodic_run_interval}")

        while True:
            time.sleep(periodic_run_interval.total_seconds())
            print(f"Synchronization started at: {datetime.now()}")
            synchronize_folders(source_folder, replica_folder, log_file)
            print(f"Synchronization complete. Next synchronization after: {periodic_run_interval}")

    except (InterruptedError, KeyboardInterrupt):
        print("Automatic synchronization was interrupted. Exiting...")

# directly running with arguments
def main():
    parser = argparse.ArgumentParser(description='Synchronize two folders.')
    parser.add_argument('source_folder', help='Path to the source folder.')
    parser.add_argument('replica_folder', help='Path to the replica folder.')
    parser.add_argument('log_file', help='Path to the log file.')
    parser.add_argument('periodic_run_interval', type=parse_day_time, help='Synchronization interval using day-time.')

    arguments = parser.parse_args()


    while True:
        try:
            print(f'Synchronization started at: {datetime.now()}')
            synchronize_folders(arguments.source_folder, arguments.replica_folder, arguments.log_file)
            print(f'Next synchronization after: {arguments.periodic_run_interval}')
            time.sleep(arguments.periodic_run_interval.total_seconds())
        except InterruptedError or KeyboardInterrupt:
            print('Error automatic synchronization,')
            break

# Press the green button in the gutter to run the script/use terminal to pass arguments directly.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        main()
    else:
        test_main()
