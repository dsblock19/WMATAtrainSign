'''Libraries'''

import board
import busio
import time
import terminalio
import json
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_matrixportal.matrixportal import MatrixPortal
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


'''Setup'''

print('Begin Setup')
# Constants
JSON_URL = "http://api.wmata.com/StationPrediction.svc/json/GetPrediction/E04?%s"
headers = {'api_key': 'af18089c0c704f729aecdbc1cd79d62d',}
CDat=[]
StDat = ''

# Matrix setup
print('Matrix Setup')
matrixportal = MatrixPortal(
    url=JSON_URL,
    headers=headers,
    status_neopixel=board.NEOPIXEL,
    debug=False,
)

print('Text Setup')
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(1, 11),
    text_color=0xEF7F31,
)


'''Functions'''

print('Functions')
def PullData():
    print()
    print("Fetching json from", JSON_URL)
    r = matrixportal.fetch()
    r = json.loads(r)
    # print(r)
    ColDeData = r
    return ColDeData

def SortData(ColDeData):
    StDat = ''
    for n in range(0,len(ColDeData['Trains'])):
        if str(ColDeData['Trains'][n]['DestinationName']) == ('Branch Ave') or str(ColDeData['Trains'][n]['DestinationName']) == ('Huntington'):
            if str(ColDeData['Trains'][n]['Min']) == ('BRD') or str(ColDeData['Trains'][n]['Min']) == ('ARR'):
                StDat += '\n' + str(ColDeData['Trains'][n]['Line']) + ' ' + str(ColDeData['Trains'][n]['Min'])
            else:
                StDat += '\n' + str(ColDeData['Trains'][n]['Line']) + ' ' + str(ColDeData['Trains'][n]['Min']) + ' Mins'
    return StDat

def SerialP(StDat):
    print(StDat)


'''Loop'''

print('Start Program')

while True:
    try:
        ColDeData = PullData()

        StDat = SortData(ColDeData)

        SerialP(StDat)

        matrixportal.set_text(StDat)

        print("\nDone!")
        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(10)
