import requests
import json
from datetime import datetime, timedelta
import calendar
import csv
import pandas as pd
import os

class ClimactaApi():
    def __init__(self, token):
        self.url_api = 'https://icrop.climacta.agr.br/api/v1/get_data/'
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'  
        }

    def get_per_date(self, start_date, end_date, latitude=None, longitude=None):
        payload = {
            'start_date': start_date,
            'end_date': end_date
        }

        if latitude or longitude is not None: 
            payload['latitude'] = latitude
            payload['longitude'] = longitude     
        
        response = requests.post(self.url_api, headers=self.headers, json=payload)
        
        # Verifica se o status code é 200 (OK)
        if response.status_code == 200:
            return WeatherData(response.json())
        
        try:
            # Tenta fazer o parse da resposta como JSON, se possível
            response_data = json.loads(response.text)
            error_message = response_data.get('messages', [{}])[0].get('message', '')
        except json.JSONDecodeError:
            # Se a resposta não for um JSON válido, lida com o erro
            error_message = "Resposta não está no formato JSON ou está vazia."

        return ('Falha na requisição:', response.status_code, error_message)

    
    def current_month_data(self):
        date_now = datetime.now()
        first_day_of_the_current_month = date_now.replace(day=1)
        last_day_of_the_current_month = date_now.replace(day=calendar.monthrange(date_now.year, date_now.month)[1])

        first_day_str = first_day_of_the_current_month.strftime('%Y-%m-%d')
        last_day_str = last_day_of_the_current_month.strftime('%Y-%m-%d')

        current_month_data = self.get_data(first_day_str, last_day_str)

        return WeatherData(current_month_data)
    
    


class WeatherData():
    def __init__(self, data):
        self.data = data

    def to_csv(self, filename):
        # Verifica se o diretório existe e cria se necessário
        directory = os.path.dirname(filename)
        if not os.path.exists(directory) and directory:
            os.makedirs(directory)
        
        # Define os nomes das colunas
        fieldnames = [
            'dt', 'lon', 'lat', 'weather_id', 'weather_main', 'weather_description', 'weather_icon',
            'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity',
            'visibility', 'wind_speed', 'wind_deg', 'wind_gust', 'clouds_all', 'rain_1h', 'sunrise', 'sunset', 'name'
        ]
        
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for entry in self.data['data']:
                row = {
                    'dt': datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                    'lon': entry['coord']['lon'],
                    'lat': entry['coord']['lat'],
                    'weather_id': entry['weather'][0]['id'],
                    'weather_main': entry['weather'][0]['main'],
                    'weather_description': entry['weather'][0]['description'],
                    'weather_icon': entry['weather'][0]['icon'],
                    'temp': entry['main']['temp'],
                    'feels_like': entry['main']['feels_like'],
                    'temp_min': entry['main']['temp_min'],
                    'temp_max': entry['main']['temp_max'],
                    'pressure': entry['main']['pressure'],
                    'humidity': entry['main']['humidity'],
                    'visibility': entry.get('visibility', ''),
                    'wind_speed': entry['wind']['speed'],
                    'wind_deg': entry['wind']['deg'],
                    'wind_gust': entry['wind'].get('gust', ''),
                    'clouds_all': entry['clouds']['all'],
                    'rain_1h': entry.get('rain', {}).get('1h', ''),
                    'sunrise': datetime.fromtimestamp(entry['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S'),
                    'sunset': datetime.fromtimestamp(entry['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S'),
                    'name': entry.get('name', '')
                }
                writer.writerow(row)

    def to_excel(self, filename):
        # Verifica se o diretório existe e cria se necessário
        directory = os.path.dirname(filename)
        if not os.path.exists(directory) and directory:
            os.makedirs(directory)
        
        # Prepara os dados para exportação
        records = []
        for entry in self.data['data']:
            record = {
                'dt': datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                'lon': entry['coord']['lon'],
                'lat': entry['coord']['lat'],
                'weather_id': entry['weather'][0]['id'],
                'weather_main': entry['weather'][0]['main'],
                'weather_description': entry['weather'][0]['description'],
                'weather_icon': entry['weather'][0]['icon'],
                'temp': entry['main']['temp'],
                'feels_like': entry['main']['feels_like'],
                'temp_min': entry['main']['temp_min'],
                'temp_max': entry['main']['temp_max'],
                'pressure': entry['main']['pressure'],
                'humidity': entry['main']['humidity'],
                'visibility': entry.get('visibility', ''),
                'wind_speed': entry['wind']['speed'],
                'wind_deg': entry['wind']['deg'],
                'wind_gust': entry['wind'].get('gust', ''),
                'clouds_all': entry['clouds']['all'],
                'rain_1h': entry.get('rain', {}).get('1h', ''),
                'sunrise': datetime.fromtimestamp(entry['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S'),
                'sunset': datetime.fromtimestamp(entry['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S'),
                'name': entry.get('name', '')
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        df.to_excel(filename, index=False, engine='openpyxl')

    def get_data(self):
        return self.data