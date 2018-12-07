import csv
import json
import requests
import pandas
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os

YEARS = []
VALUES = []
YEARS_MONTH = []
meanDict = {}

## Part 1. Getting the data and storing it in a csv file
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
def readCSVandStore():
	df = pandas.read_csv('data.csv')
	for year in df['year']:
		YEARS.append(year)
		YEARS_MONTH.append(year)
	i = 0
	for month in  df['reference_period_desc']:
		YEARS_MONTH[i] = str(YEARS_MONTH[i]) + month
		i += 1
	for value in df['Value']:
		VALUES.append(int(value.replace(',','')))

	for i in range(len(VALUES)):
		if YEARS[i] in meanDict:
			meanDict[YEARS[i]].append(VALUES[i])
		else:
			meanDict[YEARS[i]] = [VALUES[i]]

def plotChart():
	for year in meanDict:
		plt.plot(meanDict[year])
		plt.xlabel("--------- " + str(year) + " --------->")
		plt.ylabel("--------- VALUE -------->")
		plt.savefig(str(year) + '.png')
		plt.close()

	plt.plot(YEARS_MONTH, VALUES)
	plt.xlabel('Plot over the years')
	plt.savefig('plot.png')
	plt.close()

def mean():
	print "\n*************************"
	print "\tMean\n*************************"
	print "Year\t |\tMean Value"
	print "--------------------------"
	for item in meanDict:
		print str(item) + "\t | \t" + str(sum(meanDict[item]) / len(meanDict[item]))

def median():
	print "\n\n*************************"
	print "\tMedian\n*************************"
	print "Year\t |\tMedian Value"
	print "--------------------------"
	for years in meanDict:
		meanDict[years].sort()
		print str(years) + "\t | \t" +  str(meanDict[years][len(meanDict[years])//2])


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

	print('\n\n')
	print 'Prediction for the month of November:', string_predictions[10]
	absolute_error = abs(string_predictions[10] - SELECTED_DATA[10])  # gets the data for the month of Nov from both arrays
	print 'Absolute Error:', absolute_error
	r_squared = r2_score(SELECTED_DATA, string_predictions)
	print 'R Squared value:', r_squared

	STRING_MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
	plt.plot(STRING_MONTHS, SELECTED_DATA)
	plt.savefig("Prediction1.png")
	plt.close()

	linear_fit = np.polyfit(NUM_MONTHS, SELECTED_DATA, 1)
	fit_function = np.poly1d(linear_fit)
	plt.plot(STRING_MONTHS, SELECTED_DATA, 'yo', STRING_MONTHS, fit_function(NUM_MONTHS), '--k')
	plt.savefig("Prediction2.png")
	plt.close()

if __name__ == '__main__':
	if not os.path.isfile('data.csv'):
		getData()
	readCSVandStore()
	plotChart()
	mean()
	median()
	linear_reg()
