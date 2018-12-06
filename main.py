import csv
import json
import requests
import pandas
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

## Global data that we might need later. Will change this whole thing into a class later, this is to receive the results quickly at first
YEARS = []
VALUES = []

## This function basically makes the api call, gets the data in JSON format, parses it to csv and stores it in a csv file. There is a loop that you can see which calls the api multiple times with different years
def getData():
	with requests.Session() as s:
		dataFile = open('data.csv', 'w')
		count = 0
		CSV_URL = 'https://quickstats.nass.usda.gov/api/api_GET/?key=AE577233-F40D-3716-BCC3-24DA66B479F1&short_desc=TURKEYS,%20YOUNG,%20SLAUGHTER,%20FI%20-%20SLAUGHTERED,%20MEASURED%20IN%20HEAD&year__GE=1989&year__LE=2018&state_alpha=VA&freq_desc=MONTHLY&format=JSON&param=short_desc'
		download = s.get(CSV_URL)
		decoded_content = download.content.decode('utf-8')
		parsedData = json.loads(decoded_content)['data']
		writer = csv.writer(dataFile)
		for vals in parsedData:
			if count == 0:
				header = vals.keys()
				writer.writerow(header)
				count += 1
			writer.writerow(vals.values())
		dataFile.close()

## Part 2
def readCSVandPlotLineGraph():
	df = pandas.read_csv('data.csv')
	for year in df['year']:
		YEARS.append(str(year))
	i = 0
	for month in  df['reference_period_desc']:
		YEARS[i] = str(YEARS[i]) + month
		i += 1
	for value in df['Value']:
		VALUES.append( int(value.replace(',',''))/1000 ) #this will give value in thousands, we can just put that as a label
	print(len(YEARS), len(VALUES))
	plt.plot(YEARS, VALUES)
	plt.show()


# Part 3
def linear_reg():
	SELECTED_DATA = []
	df = pandas.read_csv('data.csv')
	for index, row in df.iterrows():
		pandas.to_numeric(row['Value'], errors='coerce')
		if row['year'] == np.int64(2017):
			data_string = row['Value']
			data_string = data_string.replace(',', '')
			SELECTED_DATA.append(int(data_string))

	NUM_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] #['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

	lm = LinearRegression()
	RESHAPE_MONTHS = np.reshape(NUM_MONTHS, (-1, 1))
	RESHAPE_DATA = np.reshape(SELECTED_DATA, (-1, 1))
	model = lm.fit(RESHAPE_MONTHS, RESHAPE_DATA)
	predictions = lm.predict(RESHAPE_MONTHS)

	string_predictions = []
	count = 0
	while count < 12:  # for each month in predictions adds to an array that will contain the float value of the prediction
		curr_prediction = ''.join(str(e) for e in predictions[count])
		string_predictions.append(float(curr_prediction))
		count += 1

	print('Prediction for the month of November:', string_predictions[10])
	absolute_error = abs(string_predictions[10] - SELECTED_DATA[10])  # gets the data for the month of Nov from both arrays
	print('Absolute Error:', absolute_error)
	r_squared = r2_score(SELECTED_DATA, string_predictions)
	print('R Squared value:', r_squared)

	STRING_MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
	plt.plot(STRING_MONTHS, SELECTED_DATA)
	plt.show()

	linear_fit = np.polyfit(NUM_MONTHS, SELECTED_DATA, 1)
	fit_function = np.poly1d(linear_fit)
	plt.plot(STRING_MONTHS, SELECTED_DATA, 'yo', STRING_MONTHS, fit_function(NUM_MONTHS), '--k')
	plt.show()



getData()
readCSVandPlotLineGraph()
linear_reg()

