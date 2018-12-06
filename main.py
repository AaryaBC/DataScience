import csv
import json
import requests
import pandas
import matplotlib.pyplot as plt

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

# getData()
readCSVandPlotLineGraph()