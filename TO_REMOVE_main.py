#!/usr/bin/python
#
# This program does a Google search for "quick and dirty" and returns
# 50 results.
#

import tweepy

consumer_key="bEoNxJ0v68ifQiCDeezJfg"
consumer_secret="2qwz5PkEQe8K169xkTvHQ5z0GWZrR4bLgzMQ2flrW0"

access_token="2166946788-zOgvKqPSZ8oCjc42PbhpWUzAdzJbZmzK3MxWa3S"
access_token_secret="qjXXzKKsf0dnTdMtL8IRzf3PsIeQrw9aFHLm6jLumIHPk"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print "auth twitter ok"
print api.me().name

import sqlite3

conn = sqlite3.connect('/home/pi/pegman/xgoogle-master/test.db')
print "Opened database successfully";

"""
        conn.execute('''CREATE TABLE pegman
               (URLS CHAR(300)
               );''')
"""

def is_in_db(url):
        cursor = conn.execute("SELECT * from pegman where urls ='" + url + "'")
        for row in cursor:
                return 1
        return 0

from xgoogle.search import GoogleSearch, SearchError
vibrate_pegman = 0
new_url = 0

try:
        gs = GoogleSearch("pegman")
        gs.results_per_page = 20
        results = gs.get_results()
        for res in results:
        #print res.title.encode('utf8')
        #print res.desc.encode('utf8')
                url = res.url.encode('utf8')
                print url
                d =  is_in_db(url)
                print d
                if not d:
                        conn.execute("INSERT INTO pegman (URLS) VALUES ('" + url + "')");
                        conn.commit()
                        try:
                                api.update_status(url)
                        except:pass
                        vibrate_pegman = 1
                        new_url = new_url + 1
                print
except SearchError, e:
        print "Search failed: %s" % e

print "nombre de nouvelle urls"
print new_url
if vibrate_pegman:
        import time
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)

        p = GPIO.PWM(12, 100)  # channel=12 frequency=50Hz
        p.start(0)
        try:
                for i in range(new_url):
                        for dc in range(0, 101, 5):
                            p.ChangeDutyCycle(dc)
                            time.sleep(0.1)
                        for dc in range(100, -1, -5):
                            p.ChangeDutyCycle(dc)
                            time.sleep(0.1)
                p.stop()
                GPIO.cleanup()
        except KeyboardInterrupt:
                pass
                p.stop()
                GPIO.cleanup()

