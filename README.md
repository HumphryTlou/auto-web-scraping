# Data extraction script


## Install the required libraries

Run the following commands to install the required libraries:

```bash
python3 -m pip install bs4
python3 -m pip install pandas
python3 -m pip install datetime
python3 -m pip install selenium
python3 -m pip install python-dotenv
```

## Set and configure the variables in the `.env` file

Create a `.env` file, use `.env_example` as a reference, and update the variables with the correct paths.

## Run the script manually

```bash
python3 extract_data.py 
```
This will display the output in the console and save the extracted data as a CSV file.

## Automating the script using cronjob

Ensure the extract_data.py script has executable permissions:
```bash
chmod +x extract_data.py
```

Find the Python executable path using:
```bash
which python3
```
Open the crontab
```bash
crontab -e
```

Add the following line to run the script every minute:
```bash
* * * * * /opt/homebrew/bin/python3.11 /Users/***/extract_data.py
```
The above cron job runs every minute of every hour, every day, every month, and every day of the week. Modify the schedule as required, e.g:

```bash
m h d m w    
0 * * * *    every hour
0 0 * * *    everyday at midnight
30 3 * * 0   every Sunday at 3:30 AM
*/5 * * * *  every 5 minutes
```
