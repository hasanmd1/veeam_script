## Requirements

- Python 3.12
- Used Only Standard Python libraries: `os`, `shutil`, `time`, `datetime`, `argparse`, `hashlib`, `sys`
- Implemented custom md5 hash function for security reasons

## Installation

1. Clone the repository (or download the Python script):
   ```bash
   git clone https://github.com/hasanmd1/veeam_script.git
   ```
   - if you prefer ssh
   ```bash
   git clone git@github.com:hasanmd1/veeam_script.git
   ```

## Usage

### Console

To run the program with command-line arguments, use the following command:

```bash
python/python3.12 main.py source_folder replica_folder log_file synchronization_interval
```

- `source_folder`: Path to the source folder.
- `replica_folder`: Path to the replica folder.
- `log_file`: Path to the log file where synchronization actions will be recorded.
- `synchronization_interval`: Interval for periodic synchronization, in the format of days, hours, minutes, and seconds (e.g., "0:0:1:0").

### Testing Mode (Interactive)

To run the program with interactive user input (for testing or manual execution), use the following:

```bash
python/python3.12 main.py
```

This will prompt you for the following inputs:
1. **Source folder**: Path to the source folder.
2. **Replica folder**: Path to the replica folder.
3. **Log file**: Path to the log file.
4. **Synchronization interval**: The synchronization interval (in format: "X(day(s)):Y(hour(s)):Z(minute(s)):N(second(S))").

The program will then perform synchronization based on your inputs. You can also choose to run periodic synchronization, which will continue until you interrupt the process.

## Example

1. **Interactive Mode**:
- for example for 1 minute cron
   ```bash
   Enter the source folder path:
   source
   Enter the replica folder path:
   replica
   Enter the log file path:
   logfile.txt
   Enter the synchronization interval (format: 'X(day(s)):Y(hour(s)):Z(minute(s)):N(second(S))'):
   0:0:1:0
   ```
  
   This will start the synchronization and log the actions to the specified log file. The synchronization will repeat after every 0 day, 0 hour, 1 minute and 0 second.

2. **Console Mode**:
 - for example for 1 minute cron
   ```bash
   python main.py source replica logfile.txt "0:0:1:0"
   ```

   This will run the synchronization at the specified interval.