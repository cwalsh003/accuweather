from collections import OrderedDict
from pprint import pprint

import datetime
import requests
from flask import Flask
from flask import json
import time





app = Flask(__name__)

@app.route('/data')

def getData():

	date = time.strftime("%Y/%m")
	print(date)
	date2 = date[0:-3] +"/" +  str(int(date[5:]) + 1)
	print(date2)
	# date_2 = date + datetime.timedelta(days=10)
	# print (str(date_2))

	myDict = OrderedDict()
	myNewDict = OrderedDict()
	r = requests.get("http://apidev.accuweather.com/forecasts/v1/daily/45day/335315?apikey=PSUHackathon112016&Details=true")
	r2 = requests.get('http://apidev.accuweather.com/climo/v1/summary/%s/350540?apikey=PSUHackathon112016' % date)
	r3 = requests.get('http://apidev.accuweather.com/climo/v1/summary/%s/350540?apikey=PSUHackathon112016' % date2)

	myDict = json.loads(r.text)
	myDict2 = json.loads(r2.text)
	myDict3 = json.loads(r3.text)

	pprint(myDict2)
	pprint(myDict3)

	myPrec = []
	myMax = []
	myMin = []
	string = ""
	string2 = ""

	# print(myDict['DailyForecasts'])
	for keys in myDict['DailyForecasts']:
			myNewDict[keys['Temperature']] = {}
			myMax.append(keys['Temperature']['Maximum']['Value'])
			myMin.append(keys['Temperature']['Minimum']['Value'])
			myPrec.append(keys['Day']['PrecipitationProbability'])

	checkPercent = 0

	# FIXME place holders for objects

	class crop:
		rainPerWeek = 45
		maxTemp = 75
		minTemp = 35

	for n in range(45):

		if crop.maxTemp < myMax[n] and crop.maxTemp < myMax[n+1] and crop.maxTemp < myMax[n+2]:
			sum = 0
			for i in range(7):
				sum += myPrec[i+n]
			if sum >= crop.rainPerWeek * 1.2:
				checkPercent += 10 / 42
			else:
				string += "Crop max temperature exceeded on day " + n + "\n"

		else:
			checkPercent += 20 / 42

		if crop.minTemp > myMin[n] and crop.minTemp > myMin[n+1] and crop.minTemp > myMin[n+2]:
			string += "Crop minimum temperature not reached on day " + n + "\n"
		else:
			checkPercent += 20 / 42

	for n in range(39):
		for j in range(7):

			if myPrec[j+n] > 25:
				sum += myPrec[j+n]

		if crop.rainPerWeek < sum/100:
			string += "Crop required rain per week not reached on day " + n + "\n"
		else:
			checkPercent += 60 / 39

	if checkPercent < 40:
		string2 += "Recommendation: Do Not Grow:\n"
	elif checkPercent < 70:
		string2 += "Recommendation: Grow, check condition errors:\n"
	else:
		string2 += "Recommendation: Grow:\n"


	return json.dumps(myNewDict)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)

