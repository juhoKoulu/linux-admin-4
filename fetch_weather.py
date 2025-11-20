#!/usr/bin/env python3 
import os
import requests 
import mysql.connector 
from datetime import datetime 

api_key = os.getenv("OPENWEATHER_API_KEY");
mysql_user = os.getenv("MYSQL_USER");
mysql_password = os.getenv("MYSQL_PASSWORD");

CITY = 'Helsinki' 
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={api_key}&units=metric' 

conn = mysql.connector.connect(host='localhost', user=mysql_user, password=mysql_password, database='weather_db') 
cursor = conn.cursor() 

cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (id INT 
AUTO_INCREMENT PRIMARY KEY, city VARCHAR(50), temperature FLOAT, description 
VARCHAR(100), timestamp DATETIME)''') 

response = requests.get(URL)
data = response.json()

if "main" not in data:
	print(data);
	raise ValueError("data does not contain main")

temp = data['main']['temp'] 
desc = data['weather'][0]['description'] 
timestamp = datetime.now() 

cursor.execute('INSERT INTO weather_data (city, temperature, description, timestamp) VALUES (%s, %s, %s, %s)', (CITY, temp, desc, timestamp)) 
conn.commit() 
cursor.close() 
conn.close() 

print(f'Data tallennettu: {CITY} {temp}°C {desc}')
