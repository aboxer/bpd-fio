import os
import datetime
import csv

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
          row = [None if x == 'NULL' else x for x in row]
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
