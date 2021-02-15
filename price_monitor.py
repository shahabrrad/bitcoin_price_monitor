import requests
import time
import json
URL = "https://www.binance.com/"
TIME_API = "api/v3/time"
KLINE_API = "api/v3/klines"
KLINE_REQUEST_PARAMS = {'symbol':"BTCUSDT" , 'interval': "1m" , 'startTime':'0' , 'endTime':"0"}
MILISECONDS_IN_A_MINUTE = 60 * 1000
MINUTES_IN_A_DAY = 24 * 60
time_request = requests.get(url=URL+TIME_API)
server_time = time_request.json()["serverTime"]
#server time includes miliseconds, we need to omit them
current_minute = server_time // MILISECONDS_IN_A_MINUTE
current_MILISECONDS_IN_A_MINUTE = current_minute * MILISECONDS_IN_A_MINUTE
yesterday_minute = current_MILISECONDS_IN_A_MINUTE - ( MINUTES_IN_A_DAY * MILISECONDS_IN_A_MINUTE )
#only 500 requests can be made at a time
#getting first 500 minutes
KLINE_REQUEST_PARAMS['startTime'] = str(yesterday_minute)
KLINE_REQUEST_PARAMS['endTime'] = str(yesterday_minute + 500 * MILISECONDS_IN_A_MINUTE)
first_500_minutes = requests.get(url=URL+KLINE_API, params = KLINE_REQUEST_PARAMS)
#getting second 500 minutes
KLINE_REQUEST_PARAMS['startTime'] = str(yesterday_minute + 500 * MILISECONDS_IN_A_MINUTE)
KLINE_REQUEST_PARAMS['endTime'] = str(yesterday_minute + 500 * MILISECONDS_IN_A_MINUTE * 2)
second_500_minutes = requests.get(url=URL+KLINE_API, params = KLINE_REQUEST_PARAMS)
#getting last 440 minutes
KLINE_REQUEST_PARAMS['startTime'] = str(yesterday_minute + 500 * MILISECONDS_IN_A_MINUTE * 2)
KLINE_REQUEST_PARAMS['endTime'] = str(current_MILISECONDS_IN_A_MINUTE)
last_minutes = requests.get(url=URL+KLINE_API, params = KLINE_REQUEST_PARAMS)


all_minutes = first_500_minutes.json() + second_500_minutes.json() + last_minutes.json()

minutes_passed = 0
with open('recordfile.csv','w') as file:
    file.write('start time' + ',' + 'end time' + ',' + 'price')
    file.write('\n')
    for minute in all_minutes: 
        file.write(str(minute[0]) + ',' + str(minute[6]) + ',' + minute[4])
        file.write('\n')
    print("wrote last day's data")
    while minutes_passed != MINUTES_IN_A_DAY:
        time.sleep(60)
        KLINE_REQUEST_PARAMS['startTime'] = current_MILISECONDS_IN_A_MINUTE
        KLINE_REQUEST_PARAMS['endTime'] = current_MILISECONDS_IN_A_MINUTE + MILISECONDS_IN_A_MINUTE
        current_minute_data = requests.get(url=URL+KLINE_API, params = KLINE_REQUEST_PARAMS)
        current_minute_data = current_minute_data.json()
        file.write(str(current_minute_data[0][0]) + ',' + str(current_minute_data[0][6]) + ',' + current_minute_data[0][4])
        file.write('\n')
        print("wrote minute number " + str(minutes_passed) + " data")
        minutes_passed += 1
        current_MILISECONDS_IN_A_MINUTE += MILISECONDS_IN_A_MINUTE

