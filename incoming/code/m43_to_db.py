import argparse
import re
import json
import csv
import os
import datetime
import json

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
fios = []
for file in os.listdir(args.src):
  if file.startswith("fios_"):
    inf = os.path.join(args.src, file)
    with open(inf) as f:
      reader = csv.reader(f)
      #hdr = reader.next()
      next(reader)
      for row in reader:
        ts = tsDate(row[1])
        dat = [row[0],ts,row[1]]
        dat.extend(row[2:])
        fios.append(dat)

#merge rows with duplicate fio_ids.
#if the duplicate column differs, change the column value to a list of all the different values
uniq_fios = []
uniq_ids = []
dups = []
for off,fio in enumerate(fios):
  fio_id = fio[0]
  if fio_id in uniq_ids:
    dups.append([off,fio_id])
  else:
    uniq_ids.append(fio_id)
    uniq_fios.append(fio)

for dup_off,dup_id in dups:
  dup_fio = fios[dup_off]
  uniq_off = uniq_ids.index(dup_id)
  uniq_fio = uniq_fios[uniq_off]
  for i,val in enumerate(dup_fio):
    if isinstance(uniq_fio[i], list):
      uniq_fio[i].append(val)
    else:
      if val != uniq_fio[i]:
        uniq_fio[i] = [uniq_fio[i],val]

#res = list(set(fio_ids))
with open(args.genf,'w') as f:
  json.dump(fios,f, indent=2)
exit()
#print(fios)
