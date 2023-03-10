import argparse
import re
import json
import csv
import myLib as ml
from tabulate import tabulate
import os

parser = argparse.ArgumentParser()
parser.add_argument('inf', help='file of all bpd fios')
parser.add_argument('genf', help='output database')
parser.add_argument('logf', help='reports about results')
args = parser.parse_args()

log = open(args.logf,"w")

######################### get fios ####################################
#get all the rows in all the mark43 fio files
fios = ml.getRecords(args.inf,"fios_")
fios = [x[1:] for x in fios] #2nd colum is the fio_id that we need to identify unique fios

#merge rows with duplicate fio_ids.
#if the duplicate column differs, change the column value to a list of all the different values
uniq_fios = ml.mkUniqs(fios)



with open(args.genf,'w') as f:
  json.dump(uniq_fios,f, indent=2)

log.write(f'fios = {len(fios)} uniq_fios = {len(uniq_fios)}\n')
cols = ['seq_num','fio_id','sex','location','dist','dist_id','fio_date','fio_time','priors','description','clothing','complexion','fiofs_type','terrorism','search','basis','stop_reasons','enteredby','fiofs_reasons','outcome','veh_make','veh_year_num','veh_color','veh_model','veh_occupant','veh_state','supervisor_id','officer_id','supervisor','off_dist_id','off_dist','officer','sup_entrydate','last_updateby','last_updatetime','ethnicity','first_inserttime','active_id','race_id','race_desc','fio_date_corrected','age_at_fio_corrected','street_id','city']

nums = [x for x in range(len(cols))] 
tbl = zip(cols,nums)
log.write(tabulate(tbl))

log.close()
exit()
