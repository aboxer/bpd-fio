import argparse
import re
import json
import csv
import os
import datetime
from tabulate import tabulate
import myLib as ml


parser = argparse.ArgumentParser()
parser.add_argument('src', help='directory of all bpd fios')
parser.add_argument('genf', help='output database')
parser.add_argument('logf', help='reports about results')
args = parser.parse_args()

log = open(args.logf,"w")

######################### get fios ####################################
#get all the rows in all the mark43 fio files
fios = ml.getRecords(args.src,"fios_")

#merge rows with duplicate fio_ids.
#if the duplicate column differs, change the column value to a list of all the different values
uniq_fios = ml.mkUniqs(fios)

######################### get suspects ################################
#get all the rows in all the mark43 suspect files
#2021,2022 have sligntly different format that must be fixed
raw_suss = ml.getRecords(args.src,"suss_")
suss = []
for sus in raw_suss:
  suss.append(sus[1:])

uniq_suss = ml.mkUniqs(suss)

uniq_fio_ids = []
uniq_fio_offs = []
for fio_off,fio in enumerate(uniq_fios):
  uniq_fio_ids.append(fio[0])
  uniq_fio_offs.append(fio_off)

no_fios = 0
for uniq_sus in uniq_suss:
  try:
    uniq_fio_off = uniq_fio_ids.index(uniq_sus[0])
    uniq_fios[uniq_fio_off].extend(uniq_sus[2:])
  except:
    no_fios += 1

dummy = [None]*9
no_suss = 0
for uniq_fio in uniq_fios:
  if len(uniq_fio) != 33:
    uniq_fio.extend(dummy)
    no_suss += 1
  #uniq_fio.append(ml.tsDate(uniq_fio[1])) #NOTE - I'll do this in the final stage of the pipeline if all formats are the same

with open(args.genf,'w') as f:
  json.dump(uniq_fios,f, indent=2)

log.write(f'fios = {len(fios)} uniq_fios = {len(uniq_fios)} no_suss = {no_suss} no_fios = {no_fios}\n') 
cols = ['fc_num','contact_date','contact_officer','contact_officer_name','supervisor','supervisor_name','street','city','state','zip','frisked','searchperson','searchvehicle','summonsissued','stop_duration','circumstance','basis','vehicle_year','vehicle_state','vehicle_make','vehicle_model','vehicle_color','vehicle_style','vehicle_type','contact_reason','sex','race','age','build','hair_style','complexion','ethnicity','otherclothing']

nums = [x for x in range(len(cols))] 
tbl = zip(cols,nums)
log.write(tabulate(tbl))


log.close()
exit()
