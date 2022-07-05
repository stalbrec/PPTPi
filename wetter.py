import python_weather
import asyncio
import os,csv, datetime, json
from sense_hat import SenseHat

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
        self.csv_path = f'./{self.name}_records.csv'
        self.current_records:Dict = {'pyweather':{},'sense_hat':{}}
        self.date_format = "%Y-%m-%d_%H:%M:%S"
        self.sense = SenseHat()
        self.sense.set_rotation(180)

    async def _update_pyweather(self):
        client = python_weather.Client(locale='de-DE')
        self.pyweather = await client.find(f"{self.lat},{self.long}" if self.location=='' else self.location)
        await client.close()
        
    def update_pyweather(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._update_pyweather())
        self.current_records['pyweather']={
            'Zeitpunkt':self.pyweather.current.date.strftime(self.date_format),
            'Temperatur':self.pyweather.current.temperature,
            'Temperatur_felt':self.pyweather.current.feels_like,
            'rel_Luftfeuchtigkeit':self.pyweather.current.humidity,
            'Himmelbeschreibung':self.pyweather.current.sky_text,
            'Windgeschwindigkeit':self.pyweather.current.wind_speed
            }


    def update_sense_hat(self):
        self.current_records['sense_hat']={
            'Zeitpunkt':datetime.datetime.now().strftime(self.date_format),
            'Temperatur':round(self.sense.get_temperature(),2),
            'Temperatur_hum':round(self.sense.get_temperature_from_humidity(),2),
            'Temperatur_pres':round(self.sense.get_temperature_from_pressure(),2),
            'Temperatur_cpu':get_cpu_temp(),
            'Luftdruck':round(self.sense.get_pressure(),2),
            'rel_Luftfeuchtigkeit':round(self.sense.get_humidity(),2),
            #'Himmelbeschreibung':self.pyweather.current.sky_text,
            #'Windgeschwindigkeit':self.pyweather.current.wind_speed
            }

    def update_json(self):
        with open(f'{self.name}_current_records.json','w') as jsonfile:
            json.dump(self.current_records,jsonfile,indent = 2)
            
    def update_csv(self):
        append = os.path.isfile(self.csv_path)
        with open(self.csv_path, 'a' if append else 'w', newline='') as csvfile:
            fieldnames = [f"{origin}_{variable}" for origin in self.current_records.keys() for variable in self.current_records[origin].keys() ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if(not append):
                writer.writeheader()
            row = {f"{origin}_{variable}":self.current_records[origin][variable] for origin in self.current_records.keys() for variable in self.current_records[origin].keys()}
            writer.writerow(row)
            
    def update(self):
        #self.sense.show_message("Update:")
        self.sense.show_letter("!",(255,0,0),(255,255,255))
        time.sleep(1)
        self.sense.clear()
        self.update_pyweather()
        self.update_sense_hat()
        self.update_json()
        self.update_csv()
        
        #self.sense.show_message(f"T={self.current_records['pyweather']['Temperatur']}/{self.current_records['sense_hat']['Temperatur']} C")
        #print("Update:")
        print(json.dumps(self.current_records,indent=2))

if(__name__ == '__main__'):
    import time
    
    ws = WetterStation()
    
    update_interval = 60 #seconds
    
    while True:
        ws.update()
        time.sleep(update_interval)
