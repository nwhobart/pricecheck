#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import arrow
import re
import sys
import pprint
import csv

r = requests.get('https://hourlypricing.comed.com/rrtp/ServletFeed?type=pricingtabledaynexttomorrow')
soup = BeautifulSoup(r.text, 'html.parser')
pp = pprint.PrettyPrinter(indent=2)
prices = list(re.findall(r"(...¢)",soup.text))
times = list(range(0,24))
zipped = zip(times, prices)
table = list(zip(times, prices))
sorty = sorted(zipped, key=lambda x: x[1])
csv_columns = ['time','price']

def safety_checks():
  sys.tracebacklimit = 0
  right_now = arrow.now().format('HH:mm:ss')
  if right_now <= "16:30:00":
    raise RuntimeError("ComEd publishes rates at 16:30. The time is currently: {}" .format(right_now))
    exit(1)
  if r.status_code is not 200:
    raise RuntimeError("ComEd servers are acting up. The return code is: {}" .format(r.status_code))
    exit (1)
  return safety_checks

def main():
  safety_checks()
  pp.pprint(table)
  pp.pprint(sorty)


if __name__ == "__main__":
  main()
