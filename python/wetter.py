#!/usr/bin/env python3
import python_weather
import asyncio
import os,csv, datetime, json
from sense_hat import SenseHat
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('/home/pi/PPTPi/python')
from sensors import TemperaturSensoren


def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=","").replace("'C\n",""))
    return(t)

class WetterStation(object):
    def __init__(self, name='WetterstationI',latitude=53.577758, longitude=9.886157, location=''):
        self.name = name
        self.lat = latitude
        self.long = longitude
        self.location = location
        self.pyweather = None
        self.csv_path = f'/home/pi/PPTPi/python/{self.name}_records.csv'
        self.current_records:Dict = {'pyweather':{},'sense_hat':{}}
        self.date_format = "%Y-%m-%d_%H:%M:%S"
        self.sense = SenseHat()
        self.sense.set_rotation(180)

    async def _update_pyweather(self):
        #client = python_weather.Client(locale='de-DE')
        client = python_weather.Client(format=python_weather.METRIC)
        self.pyweather = await client.get(f"{self.lat},{self.long}" if self.location=='' else self.location)
        await client.close()
        
    def update_pyweather(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._update_pyweather())
        self.current_records['pyweather']={
            'Zeitpunkt':self.pyweather.current.local_time.strftime(self.date_format),
            'Temperatur':self.pyweather.current.temperature,
            'Temperatur_felt':self.pyweather.current.feels_like,
            'rel_Luftfeuchtigkeit_py':self.pyweather.current.humidity,
            #'Himmelbeschreibung':self.pyweather.current.sky_text,
            }


    def update_sense_hat(self):
        Ts = TemperaturSensoren()

        self.current_records['sense_hat']={
            'Zeitpunkt':datetime.datetime.now().strftime(self.date_format),
            'Temperatur':round(self.sense.get_temperature(),2),
            'Temperatur_hum':round(self.sense.get_temperature_from_humidity(),2),
            'Temperatur_pres':round(self.sense.get_temperature_from_pressure(),2),
            'Temperatur_cpu':get_cpu_temp(),
            'Luftdruck':round(self.sense.get_pressure(),2),
            'rel_Luftfeuchtigkeit':round(self.sense.get_humidity(),2),
            #'Himmelbeschreibung':self.pyweather.current.sky_text,
            'Temperatur_sensor':Ts.temps()[0],
            #'Windgeschwindigkeit':self.pyweather.current.wind_speed
            }
            
    def makeplt(self):
        data = pd.read_csv('/home/pi/PPTPi/python/WetterstationI_records.csv')
        
        data['sense_hat_time'] = pd.to_datetime(data['sense_hat_Zeitpunkt'], format="%Y-%m-%d_%H:%M:%S")
        data['pyweather_time'] = pd.to_datetime(data['pyweather_Zeitpunkt'], format="%Y-%m-%d_%H:%M:%S")+datetime.timedelta(hours=1)
        
        data['sense_hat_Temperatur_average'] = (data['sense_hat_Temperatur_pres']+data['sense_hat_Temperatur_hum'])/2
        transparent = True
        f, ax = plt.subplots(figsize=(7,5))
        time = data['sense_hat_time'].dt.strftime("%H:%M").to_numpy()
        ax.plot(time, data['sense_hat_Temperatur_sensor'],label='externer Sensor')
        ax.plot(time, data['sense_hat_Temperatur'],label='SenseHat Sensor')
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Temperatur in Celsius")
        ax.legend(fancybox=True, framealpha=0.5)
        tick_points = np.linspace(0,len(time),10)
        tick_labels = time[::round(len(time)/10)] if len(time)>10 else time
        plt.xticks(tick_labels)
        f.savefig("/home/pi/PPTPi/python/Temperatur_Raum.png",transparent=transparent)
        
        f, ax = plt.subplots(figsize=(7,5))
        time = data['pyweather_time'].dt.strftime("%H:%M").to_numpy()
        ax.plot(time, data['pyweather_Temperatur'],label='Temperatur')
        ax.plot(time, data['pyweather_Temperatur_felt'],label='gefuehlte Temperatur')
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Temperatur in Celsius")
        ax.legend(fancybox=True, framealpha=0.5)
        tick_labels = time[::round(len(time)/10)] if len(time)>10 else time
        plt.xticks(tick_labels)
        f.savefig("/home/pi//PPTPi/python/Temperatur_online.png",transparent=transparent)
        

    def update_json(self):
        with open(f'/home/pi/PPTPi/python/{self.name}_current_records.json','w') as jsonfile:
            json.dump([self.current_records],jsonfile,indent = 2)
            
    def update_csv(self):
        append = os.path.isfile(self.csv_path)
        with open(self.csv_path, 'a' if append else 'w', newline='') as csvfile:
            fieldnames = [f"{origin}_{variable}" for origin in self.current_records.keys() for variable in self.current_records[origin].keys() ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if(not append):
                writer.writeheader()
            row = {f"{origin}_{variable}":self.current_records[origin][variable] for origin in self.current_records.keys() for variable in self.current_records[origin].keys()}
            writer.writerow(row)
            
    def update(self,sleep=5):
        self.sense.show_letter("!",(255,0,0),(255,255,255))

        self.update_pyweather()
        self.update_sense_hat()
        self.update_json()
        self.update_csv()
        
        self.makeplt()
        
        print(json.dumps(self.current_records,indent=2))

        alert_duration = 3
        time.sleep(alert_duration)
        self.sense.clear()
        time.sleep(max(0,sleep-alert_duration))

if(__name__ == '__main__'):
    
    ws = WetterStation(location='Hamburg')
    
    update_interval = 60 #seconds
    
    while True:
        ws.update(sleep=update_interval)
        
