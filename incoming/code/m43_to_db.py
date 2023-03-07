import argparse
import re
import json
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument('src', help='directory of all bpd fios')
parser.add_argument('genf', help='output database')
args = parser.parse_args()


fio_id = 0
fios = []
for file in os.listdir(args.src):
  if file.startswith("fios_"):
    inf = os.path.join(args.src, file)
    with open(inf) as f:
      reader = csv.reader(f)
      hdr = reader.next()
      for row in reader:
        #fios.append([row[fio_id]])
        fios.append(row[fio_id])

res = list(set(fios))
#res = [*set(fios)]
print(fios)
