# Python program to find current
# weather details of any city with city id
# using open-weather-map api

# import required modules
import requests
import pandas as pd
import xlwings as xw
from time import sleep

df = pd.read_json("current.city.list.json.gz")

md = df["id"][:]
kd = df["id"][:5]
li = list(md)
dc = pd.DataFrame({"CITY-ID": li})
flag = False
m = 1
n = "C"
humidity_s = []
temperatures = []
city_names = []
units = []
update = []
wb = xw.Book('temp.xlsx')
ws1 = wb.sheets['sheet1']
# ws2 = wb.sheets['sheet2']
# ws3 = wb.sheets['sheet3']

while True:
    for i in kd:

        if flag:
            m = ws1.range(f'F{str(i)}').options(numbers=int).value

        if m == 1:
            if flag:
                n = ws1.range(f'E{str(i)}').options.value
            if n == "C":
                unit = "metric"
            else:
                unit = "imperial"
                # Enter your API key here
                api_key = "ac7c75b9937a495021393024d0a90c44"

                # base_url variable to store url
                # we can also use api for more city at one time
                base_url = "http://api.openweathermap.org/data/2.5/weather?"

                # Give city name
                city_id = str(i)  # I have used City Id you can also use City name by change little code in complete url

                # complete url address, Here instead of id You can Use city name by removing "id=" and just city_name
                complete_url = base_url + "id=" + city_id + "&units=" + unit + "&appid=" + api_key

                # response object
                response = requests.get(complete_url)

                # convert json format data into
                # python format data
                js = response.json()

                # Check the value of "cod" key is equal to
                # "404", means city is found otherwise,
                # city is not found
                if js["cod"] != "404":

                    # store the value of "main"
                    # key in variable y
                    find = js["main"]

                    # store the value corresponding
                    # to the "temp" key of y
                    current_temperature = find["temp"]

                    # store the value corresponding
                    # to the "humidity" key of y
                    current_humidity = find["humidity"]

                    # store the value of "city-name"
                    # key in variable z
                    z = js["name"]

                    if unit == "metric":
                        t = "C"
                    else:
                        t = "F"
                    units.append(t)

                    temperatures.append(str(current_temperature))
                    humidity_s.append(str(current_humidity))
                    city_names.append(str(z))
                    update.append(str(1))

                else:
                    print(" City Not Found ")

    dm = pd.DataFrame({"CITY": city_names,
                       "TEMPERATURE": temperatures,
                       "HUMIDITY": humidity_s,
                       "UNIT": units,
                       "UPDATE": update
                       })
    # print(dm)""

    ws1.range('A1').value = dm
    # ws2.range("A1").value = dc
    # ws3.range('A1').value = 'I have Just taken first 5 city of current.city.list.json.gz,' \
    #                         ' you can change according to you.'
    wb.save("temp.xlsx")
    flag = True
    sleep(5)
