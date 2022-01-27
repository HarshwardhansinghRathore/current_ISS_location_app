import requests
from datetime import datetime
import smtplib
import time
import os

iss_response = requests.get(url='http://api.open-notify.org/iss-now.json')
json_data = iss_response.json()['iss_position']
iss_location = (float(json_data['longitude']), float(json_data['latitude']))
parameters = {
        'lat': 20.593683,
        'lng': 78.962883,
        'formatted': 0
    }


def is_it_night():
    now = datetime.now().hour
    sunrise_response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    sunrise_response.raise_for_status()
    sunrise = int(sunrise_response.json()['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(sunrise_response.json()['results']['sunset'].split('T')[1].split(':')[0])
    if now >= sunset or now <= sunrise:
        return True
    else:
        return False


while True:
    time.sleep(60)
    if abs(iss_location[1] - parameters['lat']) < 5 and abs(iss_location[0] - parameters['lng']) < 5 and is_it_night():
        connection = smtplib.SMTP('smtp.gmail.com', port=587)
        connection.starttls()
        connection.login(user='hr@gmail.com', password=os.environ['PASSWORD'])
        connection.sendmail(from_addr='hr1566027@gmail.com', to_addrs='hr32602@gmail.com',
                            msg='Subject:ISS above you\n\ngo out and see the international space station is above you '
                                'may be you can see it')
