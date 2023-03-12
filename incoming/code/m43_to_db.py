import argparse
import re
import json
import csv
import os
import datetime
import json
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
suss = ml.getRecords(args.src,"suss_f1_")
suss_f2 =  ml.getRecords(args.src,"suss_f2_")
for sus in suss_f2:
  tmp = [sus[2],sus[1],sus[3],sus[4],sus[5],sus[6],sus[7],sus[9],sus[8],None,sus[10],sus[12],sus[11],sus[13]]
  suss.append(tmp)
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

dummy = [None]*12
no_suss = 0
for uniq_fio in uniq_fios:
  if len(uniq_fio) != 34:
    uniq_fio.extend(dummy)
    no_suss += 1
  #uniq_fio.append(ml.tsDate(uniq_fio[1])) #NOTE - I'll do this in the final stage of the pipeline if all formats are the same

with open(args.genf,'w') as f:
  json.dump(uniq_fios,f, indent=2)

log.write(f'fios = {len(fios)} uniq_fios = {len(uniq_fios)} suss = {len(suss)} uniq_suss = {len(uniq_suss)} no_suss = {no_suss} no_fios = {no_fios}\n') 
cols = ['fc_num','contact_date','contact_officer','contact_officer_name','supervisor','supervisor_name','street','city','state','zip','stop_duration','circumstance','basis','vehicle_year','vehicle_state','vehicle_model','vehicle_color','vehicle_style','vehicle_type','key_situations','narrative','weather','sex','race','age','build','hair_style','skin_tone','ethnicity','otherclothing','deceased','license_state','license_type','frisk/search']
nums = [x for x in range(len(cols))] 
tbl = zip(cols,nums)
log.write(tabulate(tbl))


log.close()
exit()
