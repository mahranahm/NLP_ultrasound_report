import glob
import csv
import os
import pandas as pd
read_files = glob.glob('./*.txt')

with open("convert_sample.csv", "w") as outfile:
    #w= csv.DictWriter(outfile, fieldnames=column_names)
    w = csv.writer(outfile)
    w.writerow(["reports_path"])
    for f in read_files:
        with open(f, "rb") as infile:
            w.writerow([b" ".join([line.strip() for line in infile])])
