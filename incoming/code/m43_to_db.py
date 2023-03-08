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

######################### helper functions ############################
#create a timestamp from the date = yyyy-mm-dd hr:min:sec
def tsDate(date):
  dt = datetime.datetime.strptime( date, "%Y-%m-%d %H:%M:%S")
  ts = datetime.datetime.timestamp(dt)
  return ts

#get the records
def getRecords(src_dir,file_prefix):
  fios = []
  for file in os.listdir(src_dir):
    if file.startswith(file_prefix):
      inf = os.path.join(src_dir, file)
      with open(inf) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
          fios.append(row)
  return fios

def mkUniqs(fios):
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
	  return uniq_fios

######################### get fios ####################################
#get all the rows in all the mark43 fio files
fios = getRecords(args.src,"fios_")

#merge rows with duplicate fio_ids.
#if the duplicate column differs, change the column value to a list of all the different values
uniq_fios = mkUniqs(fios)

######################### get suspects ################################
#get all the rows in all the mark43 suspect files
#2021,2022 have sligntly different format that must be fixed
suss = getRecords(args.src,"suss_f1_")
suss_f2 =  getRecords(args.src,"suss_f2_")
for sus in suss_f2:
  tmp = [sus[2],sus[1],sus[3],sus[4],sus[5],sus[6],sus[7],sus[9],sus[8],None,sus[10],sus[12],sus[11],sus[13]]
  suss.append(tmp)
uniq_suss = mkUniqs(suss)

uniq_fio_ids = []
uniq_fio_offs = []
for fio_off,fio in enumerate(uniq_fios):
  uniq_fio_ids.append(fio[0])
  uniq_fio_offs.append(fio_off)

for uniq_sus in uniq_suss:
  try:
    uniq_fio_off = uniq_fio_ids.index(uniq_sus[0])
    uniq_fios[uniq_fio_off].extend(uniq_sus[2:])
  except:
    pass

with open(args.genf,'w') as f:
  json.dump(uniq_fios,f, indent=2)
print(len(fios),len(uniq_fios))
exit()
