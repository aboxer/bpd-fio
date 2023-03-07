proot := $(shell git rev-parse --show-toplevel)/
in_dir := $(proot)src/
app_dir := $(proot)incoming/
code_dir := $(app_dir)code/
gen_dir := $(app_dir)gen/
out_dir := $(app_dir)output/
dbg_dir := $(app_dir)debug/

ifdef dbg
	mpdb := -mpdb
endif

.PHONY: db m43 rms old

m43: $(code_dir)m43_to_db.py
	touch $(code_dir)m43_to_db.py
	python $(mpdb) $(code_dir)m43_to_db.py \
	  $(in_dir)mark43 \
		$(gen_dir)m43_db.json

rms: $(code_dir)rms_to_db.py
	touch $(code_dir)rms_to_db.py
	python $(mpdb) $(code_dir)rms_to_db.py \
	  $(in_dir)new_rms \
		$(gen_dir)rms_db.json

old: $(code_dir)old_to_db.py
	touch $(code_dir)old_to_db.py
	python $(mpdb) $(code_dir)old_to_db.py \
	  $(in_dir)old_rms/fios_2011_15.csv \
		$(gen_dir)old_db.json

