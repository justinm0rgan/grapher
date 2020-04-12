# To use this program, the arguments are as follows...
# python3 precip_app.py <CSV FILE> <DATE COLUMN NUMBER> <PRECIPITATION COLUMN NUMBER> <TMIN COLUMN NUMBER> <TMAX COLUMN NUMBER> <CHART TITLE> <OUTPUT IMAGE FILENAME>
#
# Example usage:
# python3 precip_app.py 'data/sitka_weather_2018_simple.csv' 2 3 5 6 "Daily temperature average and precipitation - 2018, Sita, AK" "sitka_temp_precipitation_2018.png"

import csv
import matplotlib.pyplot as plt
import sys
from datetime import datetime
from dateutil.parser import parse


# Get all the input from the user
csv_file = sys.argv[1]
date_column_number = int(sys.argv[2])
precip_data_column_number = int(sys.argv[3])
tmin_data_column_number = int(sys.argv[4])
tmax_data_column_number = int(sys.argv[5])
chart_title = sys.argv[6]
output_png_file_name = sys.argv[7]

with open(csv_file) as f:
	reader = csv.reader(f)
	header_row = next(reader)

    # Get dates and precipitation data
	dates, prcps, tavg = [],[], []

	for row in reader:
		parsed_date = parse(row[date_column_number])
		datetime.strftime(parsed_date, '%Y-%m-%d')

		try:
			parsed_precipitation = float(row[precip_data_column_number])
			temperature_low = int(row[tmin_data_column_number])
			temperature_high = int(row[tmax_data_column_number])
		except ValueError:
			print(f"Missing data for {parsed_date}")
		else:
			if parsed_date != None:
				dates.append(parsed_date)
			prcps.append(parsed_precipitation)
			tavg.append((temperature_low+temperature_high)/2)

# Plot the points for precipitation
plt.style.use('seaborn')
fig, ax1 = plt.subplots(figsize=(15,9))
color = 'tab:red'
ax1.set_xlabel("Date (s)", fontsize=16)
ax1.set_ylabel("Precipitation (IN)", color=color, fontsize=16)
ax1.plot(dates, prcps, label="Precipitation",color=color)

ax2 = ax1.twinx() # instantiate a second axis that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel("Degrees", color=color, fontsize=16)
ax2.plot(dates, tavg, label="Avg Temp",color=color)
ax2.tick_params(axis='y', labelcolor=color)

ax1.legend()
ax2.legend()

# Format title
title = chart_title
plt.title(title, fontsize=24)

# Format the ticks
plt.tick_params(axis='both', which='major', labelsize=16)
fig.autofmt_xdate()


plt.savefig('./output/' + output_png_file_name, bbox_inches='tight')
plt.show()