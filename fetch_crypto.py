#!/usr/bin/env python3 
import os
import requests 
import mysql.connector 
from datetime import datetime 

api_key = os.getenv("COINLAYER_API_KEY");
mysql_user = os.getenv("MYSQL_USER");
mysql_password = os.getenv("MYSQL_PASSWORD");

URL = f'https://api.coinlayer.com/api/live?access_key={api_key}' 

conn = mysql.connector.connect(host='localhost', user=mysql_user, password=mysql_password, database='crypto_db') 
cursor = conn.cursor() 

cursor.execute('''CREATE TABLE IF NOT EXISTS exchange_rate (id INT 
AUTO_INCREMENT PRIMARY KEY, coin VARCHAR(50), rate FLOAT, timestamp DATETIME)''') 

response = requests.get(URL)
data = response.json()

if "success" not in data:
	print(data);
	raise ValueError("data does not contain success")

if data["success"] == False:
	print(data);
	raise ValueError("api returned success = false")

if "rates" not in data:
	raise ValueError("data does not contain rates")

for coin, rate in data["rates"].items():
	timestamp = datetime.now() 
	cursor.execute('INSERT INTO exchange_rate (coin, rate, timestamp) VALUES (%s, %s, %s)', (coin, rate, timestamp)) 
	print(f'Data tallennettu: {coin} {rate} {timestamp}')

conn.commit() 
cursor.close() 
conn.close() 
