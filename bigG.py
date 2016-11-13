from collections import OrderedDict
from pprint import pprint

import datetime
import requests
from flask import json
import time

from flask import request, Flask, jsonify

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



	# print(myDict['DailyForecasts'])
	for keys in myDict['DailyForecasts']:
			myNewDict[keys['Date']] = {}
			myNewDict[keys['Date']]['Temperature']={}
			myNewDict[keys['Date']]['Temperature']['Maximum']=keys['Temperature']['Maximum']['Value']
			myNewDict[keys['Date']]['Temperature']['Minimum']=keys['Temperature']['Minimum']['Value']
			myNewDict[keys['Date']]['Precipitation']=keys['Day']['PrecipitationProbability']


	return json.dumps(myNewDict)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)
