import requests
import json
import smtplib
from datetime import datetime

# Get current date
now = datetime.now()
# Format the date as "Month day, Year"
formatted_date = now.strftime("%B %d, %Y")

# Import values from the configuration file
with open("config.json") as json_file:
    config = json.load(json_file)
api_key = config["api_key"]
email_address = config["email_address"]
email_password = config["email_password"]
recipient_emails = config["recipient_emails"]
recipient_emails = ",".join(recipient_emails)
location = config["location"]


# Function to get weather data from API
def get_weather_data(p_location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={p_location}&appid={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# Function to send email
def send_email(subject, body):
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(email_address, recipient_emails, message)
    server.quit()

# Get weather data for Casablanca
location = "Casablanca, Morocco"
data = get_weather_data(location)

# Extract relevant information from data
temperature = data['main']['temp']
wind_speed = data['wind']['speed']
humidity = data['main']['humidity']
rain_probability = data['clouds']['all']

# Create email body
body = f"Temperature: {temperature}\nWind Speed: {wind_speed}\nHumidity: {humidity}\nRain Probability: {rain_probability}%"

# Send email with warning if rain probability is greater than 50%
if rain_probability > 50:
    subject = f"Weather Warning: High Chance of Rain  : {formatted_date}"
    body = "WARNING: High chance of rain today.\n\n" + body
    send_email(subject, body)
else:
    subject = f"Weather Update : {formatted_date}"
    send_email(subject, body)
