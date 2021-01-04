import difflib
from mitmproxyscanandread import scancoomandsfromfile
import csv


list = (scancoomandsfromfile.makeCommands())
print(list[0])
with open('./Payloads/XSS_Payloads.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile,delimiter = '\t')
    for row in spamreader:
        similarity = difflib.SequenceMatcher(None, list[0], row[0]).ratio()
        print(row[0])
        print(similarity*100)