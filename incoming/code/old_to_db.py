import argparse
import re
import json
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument('inf', help='file of all bpd fios')
parser.add_argument('genf', help='output database')
args = parser.parse_args()


fio_id = 1
fios = []
with open(args.inf) as f:
  reader = csv.reader(f)
  hdr = reader.next()
  for row in reader:
    #fios.append([row[fio_id]])
    fios.append(row[fio_id])

res = list(set(fios))
print(fios)
