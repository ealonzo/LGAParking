#!/usr/bin/env python3

from selenium import webdriver
import time
from datetime import datetime
import csv
import thingspeak
from githubkey import GITHUB_KEY, GITHUB_CHANID

# ThingSpeak values
write_key = GITHUB_KEY
channel_id = GITHUB_CHANID

# Set up browser
browser = webdriver.PhantomJS()

# Go to LaGuardia parking page
browser.get('http://laguardiaairport.com/getting-to-from/parking/')

# Need to sleep to allow javascript to load on page
time.sleep(120)

# Find P10 % utilization on page
p10percent = browser.find_element_by_css_selector('#post-10 > div > ul > li:nth-child(4) > div > h3 > span.parking-lot__id-and-percentage > span.parking-lot__percentage.u-hidden.js-lga-parking-percentage > span > span > span.parking-capacity__text > span:nth-child(1)')

# Record time
currentTime = datetime.now().strftime('%m/%d/%Y %I:%M %p')


# Function to publish to ThingSpeak
def publish(channel):

    try:
        response = channel.update({1:p10percent.text})

    except:
        print('Connection failed')

# Set up ThingSpeak format and set to "channel variable"
channel = thingspeak.Channel(id=channel_id,write_key=write_key)


# Publish result to ThingSpeak
publish(channel)

# Write to a CSV file
with open(r'/home/pi/LGAP10/p10data.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([currentTime,p10percent.text])

# Close browser
browser.quit()
