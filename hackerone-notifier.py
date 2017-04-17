#!/usr/bin/env python

'''
Pushover friendly fork of https://github.com/VincentDS/HackerOne-Notifier
'''

import urllib2
import requests
import json
import pickle
import time
import os.path
import config

dump_file = os.path.dirname(os.path.realpath(__file__)) + "/programs.dat"
ptoken = "PUSHOVER_TOKEN"
pkey = "PUSHOVER_APP_KEY"

def create_url():
  url = "https://hackerone.com/programs/search?"
  trailer = "&sort=published_at%3Adescending&limit=1000"
  filter_type = config.HACKERONE_FILTER
  url = url + "query=" + filter_type + "%3A" + config.filters[filter_type] + "&" + trailer
  return url

def retrieve_programs():
  url = create_url()
  opener = urllib2.build_opener()
  opener.addheaders = [('Accept','application/json, text/javascript, */*; q=0.01'),('content-type','application/json'),('x-requested-with','XMLHttpRequest')]
  response = opener.open(url).read()
  data = json.loads(response, encoding='latin-1')
  return data['results']

def save_programs(programs):
  dump = open(dump_file, "wb+") 
  pickle.dump(programs, dump)

def load_programs():
  dump = open(dump_file, "rb") 
  programs = pickle.load(dump)
  return programs

def check_new_programs(old, new):
  return len(new) - len(old)

def notificate_message(string):
  payload = {'token': ptoken, 'user': pkey, 'message': string, 'sound': 'incoming'}
  r = requests.post("https://api.pushover.net/1/messages.json", params=payload)

def notificate_program(program):
  text = program['name'] + " is now on HackerOne!"
  url = "https://hackerone.com" + program['url']
  payload = {'token': ptoken, 'user': pkey, 'message': text, 'sound': 'incoming'}
  r = requests.post("https://api.pushover.net/1/messages.json", params=payload)

def loop():
  while True:
    old = load_programs()
    new = retrieve_programs()
    amount_new = check_new_programs(old, new)
    if (amount_new > 0):
      for i in range(0, amount_new):
        notificate_program(new[i])
      save_programs(new)
    time.sleep(config.REFRESH_RATE)

def main():
  
  if not(os.path.isfile(dump_file)): 
    programs = retrieve_programs()
    save_programs(programs)

  notificate_message("Notifier started!")
  loop()


if __name__ == "__main__":
  main()