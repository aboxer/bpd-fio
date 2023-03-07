import argparse
import re
import json
import csv
import os
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('src', help='directory of all bpd fios')
parser.add_argument('genf', help='output database')
args = parser.parse_args()

#create a timestamp from the date = yyyy-mm-dd hr:min:sec
def tsDate(date):
  dt = datetime.datetime.strptime( date, "%Y-%m-%d %H:%M:%S")
  ts = datetime.datetime.timestamp(dt)
  return ts

#get all the rows in all the mark43 format files
fio_id = 0
fio_date = 1
fios = []
for file in os.listdir(args.src):
  if file.startswith("fios_"):
    inf = os.path.join(args.src, file)
    with open(inf) as f:
      reader = csv.reader(f)
      #hdr = reader.next()
      next(reader)
      for row in reader:
        ts = tsDate(row[fio_date])
        fios.append([row[fio_id],ts,row[fio_date]])

#merge rows with duplicate fio_ids.
#if the duplicate column differs, change the column value to a list of all the different values
uniqs = []
dups = []
for i,fio in enumerate(fios):
  val = fio[fio_id]
  if val in uniqs:
    dups.append([i,val])
  else:
    uniqs.append(val)

res = list(set(fio_ids))
print(fios)
