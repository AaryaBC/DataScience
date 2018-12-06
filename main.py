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
		year = 1989
		dataFile = open('data.csv', 'w')
		count = 0
		while year < 2019:
			dataYear = str(year)
			CSV_URL = 'https://quickstats.nass.usda.gov/api/api_GET/?key=AE577233-F40D-3716-BCC3-24DA66B479F1&commodity_desc=TURKEYS&short_desc=TURKEYS,%20YOUNG,%20SLAUGHTER,%20FI%20-%20SLAUGHTERED,%20MEASURED%20IN%20HEAD&year__GE=' +  dataYear + '&state_alpha=VA&format=JSON&param=short_desc'
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
			year += 1
		dataFile.close()

def readCSV():
	df = pandas.read_csv('data.csv')
	for year in df['year']:
		YEARS.append(year)
	for value in df['Value']:
		VALUES.append( int(value.replace(',',''))/1000 ) #this will give value in thousands, we can just put that as a label

	plt.plot(YEARS, VALUES)
	plt.show()

getData()
readCSV()