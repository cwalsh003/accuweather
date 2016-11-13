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
    date2 = date[0:-3] + "/" + str(int(date[5:]) + 1)
    print(date2)
    # date_2 = date + datetime.timedelta(days=10)
    # print (str(date_2))

    myDict = OrderedDict()
    myNewDict = OrderedDict()
    r = requests.get(
        "http://apidev.accuweather.com/forecasts/v1/daily/45day/335315?apikey=PSUHackathon112016&Details=true")
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

    # print(myDict['DailyForecasts'])
    for keys in myDict['DailyForecasts']:
        # myNewDict[keys['Temperature']] = {}
        myMax.append(keys['Temperature']['Maximum']['Value'])
        myMin.append(keys['Temperature']['Minimum']['Value'])
        myPrec.append(keys['Day']['PrecipitationProbability'])

    checkPercent = 0
    cropMax = 0
    cropMin = 0
    cropPrec = 0

    # FIXME place holders for objects

    class crop:
        rainPerWeek = 45
        maxTemp = 75
        minTemp = 35

    for n in range(39):

        if crop.maxTemp < myMax[n] and crop.maxTemp < myMax[n + 1] and crop.maxTemp < myMax[n + 2]:
            requiredrain = 0
            for i in range(7):
                requiredrain += myPrec[i + n]
            if requiredrain >= crop.rainPerWeek * 1.2:
                checkPercent += 10 / 42
            else:
                cropMax += 1
        else:
            checkPercent += 20 / 42

        if crop.minTemp > myMin[n] and crop.minTemp > myMin[n + 1] and crop.minTemp > myMin[n + 2]:
            cropMin += 1
        else:
            checkPercent += 20 / 42

    for n in range(39):
        for j in range(7):
            rainneeded = 0
            if myPrec[j + n] > 25:
                rainneeded += myPrec[j + n]
        if crop.rainPerWeek < rainneeded / 100:
            cropPrec += 1
        else:
            checkPercent += 60 / 39

    if checkPercent < 40:
        string += "Recommendation: Do Not Grow:\n"
    elif checkPercent < 70:
        string += "Recommendation: Grow, check condition errors:\n"
    else:
        string += "Recommendation: Grow:\n"

    if cropMax != 0:
        string += "This crop's max temperature is exceeded for " + cropMax + " days during this period.\n"
    if cropMin != 0:
        string += "This crop's minimum temperature is not meet for " + cropMin + " days during this period.\n"
    if cropPrec != 0:
        string += "This crop's required rain per week is not meet for " + cropPrec + " days during this period.\n"

    return json.dumps(string)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
