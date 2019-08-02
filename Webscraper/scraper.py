import requests
import urllib.request
import time
from bs4 import BeautifulSoup

#Sets the URL for the scrape
url = 'https://www.islamicfinder.org/world/united-states/4174715/tallahassee-prayer-times/'

#Connects to the URL
response = requests.get(url)

#Parses the HTML code and saves it to the created soup object
soup = BeautifulSoup(response.text, "html.parser")

#Finds specified instances of the <span> subclass
#Parses the text from the line of HTML code

FAJR    = soup.findAll('span')[28]
f_time  = FAJR.text

SUNRISE = soup.findAll('span')[30]
s_time  = SUNRISE.text

DHUHR   = soup.findAll('span')[32]
d_time  = DHUHR.text

ASR     = soup.findAll('span')[34]
a_time  = ASR.text

MAGHRIB = soup.findAll('span')[36]
m_time  = MAGHRIB.text

ISHA    = soup.findAll('span')[38]
i_time  = ISHA.text

QIYAM   = soup.findAll('span')[40]
q_time  = QIYAM.text

print("Fajr Prayer Time: " + f_time)
print("Sunrise Prayer Time: " + s_time)
print("Dhuhr Prayer Time: " + d_time)
print("Asr Prayer Time: " + a_time)
print("Maghrib Prayer Time: " + m_time)
print("Isha Prayer Time: " + i_time)
print("Qiyam Prayer Time: " + q_time)
