import difflib

from mitmproxyscanandread import scancoomandsfromfile
import csv


list = (scancoomandsfromfile.makeCommands())
print(list[2])
with open('./Payloads/SQLi_Payloads.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        similarity = difflib.SequenceMatcher(None, 'aaaaaaaa', row).ratio()
        print(similarity*100)