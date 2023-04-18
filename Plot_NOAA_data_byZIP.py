'''
Created on Apr. 18, 2023

@author: raymond
'''

from geopy.geocoders import Nominatim
from noaa_sdk import noaa
import sqlite3
import datetime
import re
import pandas
import matplotlib.pyplot as plt

def main():
    
    # Asks user for zipcode
    location = get_zipcode()
    zipcode = location[0]
    details = location[1]
    print(f'Location for weather data: {details}')
    
    # Runs BuildWeatherDB but it's a function
    build_database(zipcode)
    
    # Put the relevant data in a comma separated values file
    extract_temp_humidity()
    
    # Read the data file
    datafile = pandas.read_csv("formatdata.csv")
    
    # Plot the data from the file
    plot_data(datafile, location)
    while True:
        ans = input('Plot again? (Yes/No)\n:    ')
        if ans in ['Yes', 'yes', 'y', 'Y', 'ye']:
            plot_data(datafile, location)
        else:
            print('OK. Ending program')
            break

def plot_data(datafile, location):
    print("Plots available:\nBox Plot (BOX)\nTemperature VS Humidity (TVH)\nHumidity Histogram (HH)\nHumidity Scatter Plot (HSP)")
    choice = input("What plot do you want to see? Select from options and enter corresponding key in brackets.\n:    ")
    if choice == "BOX":
        show_boxplot(datafile, location)
    elif choice == "TVH":
        show_temp_vs_humidity(datafile, location)
    elif choice == "HH":
        show_humidity_histogram(datafile, location)
    elif choice == "HSP":
        show_scatter(datafile, location)
    else:
        print("That plot-key is not recognised.")
        return main()

def show_boxplot(datafile, location):
    datafile.boxplot(); plt.suptitle('Box plot')
    plt.suptitle(f'{location}\nBoxplot')
    plt.show()

def show_temp_vs_humidity(datafile, location):
    plt.figure(); datafile.Celsius.plot(label = 'Temperature'); datafile['Humidity'].plot(label = 'Humidity'); plt.legend(loc='best');
    plt.suptitle(f'{location}\nCelsius VS Humidity')
    plt.show()

def show_humidity_histogram(datafile, location):
    datafile['Humidity'].hist(bins=10, alpha=0.5); plt.suptitle('Histogram of Humidity')
    plt.suptitle(f'{location}\nHumidity Histogram')
    plt.show()

def show_scatter(datafile, location):
    plt.scatter(datafile.index.values,datafile['Humidity']); plt.suptitle('Humidity')
    plt.suptitle(f'{location}\nHumidity Scatterplot')
    plt.show()

def extract_temp_humidity():
    print('Extracting data.\n')
    #file names for database and output file
    dbFile = "weather.db"
    output_file_name='formatdata.csv'
    
    #connect to and query weather database and 
    conn = sqlite3.connect(dbFile)
    
    #create cursor to execute SQL commands
    cur = conn.cursor()
    
    selectCmd = """ SELECT temperature, relativeHumidity FROM observations ORDER BY timestamp; """
    cur.execute(selectCmd)
    allRows = cur.fetchall()
    
    # limit the number of rows output to half
    # rowCount = len(allRows)//2 # double slash does integer division
    # rows = allRows[rowCount:]
    
    rows = allRows
    
    #write data to output file
    with open(output_file_name,"w+") as outf:
        outf.write('Celsius,Fahrenheit,Humidity')
        outf.write('\n')
        print('Writing data.\n')
        for row in rows:
            tempC = row[0]
            if tempC is None:     #handle missing temperature value
                continue
            else:
                tempF = convertCtoF(tempC)
                outf.write(str(tempC)+',')
                outf.write(str(tempF)+',')
                humidity = row[1]
                if humidity is None:       #handle missing humidity value
                    outf.write('\n')
                else:
                    outf.write(str(humidity)+'\n')  #print data to file separated by commas
    
    print("Data Extracted.\n")

def convertCtoF(tempC):
    return (tempC*9.0/5.0) + 32.0

def build_database(zipCode):
    
    # date-time format is yyyy-mm-ddThh:mm:ssZ, times are Zulu time (GMT)
    # gets the most recent 14 days of data
    today = datetime.datetime.now()
    past = today - datetime.timedelta(days=14)
    startDate = past.strftime("%Y-%m-%dT00:00:00Z")
    endDate = today.strftime("%Y-%m-%dT23:59:59Z")
    country = 'US'
    
    # create connection - this creates database if not exist
    print("Preparing database...")
    dbFile = "weather.db"
    conn = sqlite3.connect(dbFile)
    
    # create cursor to execute SQL commands
    cur = conn.cursor()
    
    # drop previous version of table if any so we start fresh each time
    dropTableCmd = "DROP TABLE IF EXISTS observations;"
    cur.execute(dropTableCmd)
    
    # create new table to store observations
    createTableCmd = """ CREATE TABLE IF NOT EXISTS observations (
    timestamp TEXT NOT NULL PRIMARY KEY,
    windSpeed REAL,
    temperature REAL,
    relativeHumidity REAL,
    windDirection INTEGER,
    barometricPressure INTEGER,
    visibility INTEGER,
    textDescription TEXT
    ) ; """
    cur.execute(createTableCmd)
    print("Database prepared")
    
    # Get hourly weather observations from NOAA Weather Service API
    print("Getting weather data...")
    n = noaa.NOAA()
    observations = n.get_observations(zipCode,country,startDate,endDate)
    
    # populate table with weather observations
    print("Inserting rows...")
    insertCmd = """ INSERT INTO observations
    (timestamp, windSpeed, temperature, relativeHumidity,
    windDirection, barometricPressure, visibility, textDescription)
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?) """
    count = 0
    for obs in observations:
        insertValues = (obs["timestamp"],
                        obs["windSpeed"]["value"],
                        obs["temperature"]["value"],
                        obs["relativeHumidity"]["value"],
                        obs["windDirection"]["value"],
                        obs["barometricPressure"]["value"],
                        obs["visibility"]["value"],
                        obs["textDescription"])
        cur.execute(insertCmd, insertValues)
        count += 1
        if count > 0:
            cur.execute("COMMIT;")
            print(count, "rows inserted")
    print("Database load complete!")

def get_zipcode(): # Get and validate a zipcode from the user, return a valid zipcode and details about the zipcode
    
    zipcode = input('Enter the ZIP code of the area to gather weather data from.\n:    ')
    pattern = '^[0-9]{5}(-[0-9]{4})?$'
    result = re.match(pattern, zipcode)
    if not result:
        print('That is not a valid ZIP code. Please try again.\n\n')
        return get_zipcode()
    else:
        print(f'{zipcode} is a valid ZIP code.\nGeting details on chosen location.')
        geolocator = Nominatim(user_agent="CEIS110Project")
        location = geolocator.geocode(int(zipcode))
        print(f'Details about ZIP code: {location}')
        ans = input('Is this the correct location? (Yes/No)\n:    ')
        if ans in ['Yes', 'yes', 'y', 'Y', 'ye']:
            return zipcode, location
        else:
            print('OK, try again then.\n\n')
            return get_zipcode()

if __name__=='__main__':
    main()


