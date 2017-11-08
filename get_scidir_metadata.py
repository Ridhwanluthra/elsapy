from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import pickle

## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])

scidir = pickle.load(open("scidir_search_results.p", "rb"))[2][:57512]

list_raw_data = list()
index = 0

import os
if "scidir_metadata.p" in os.listdir():
    old = pickle.load(open("scidir_metadata.p", "rb"))
else:
    old = None

import time
range_time = time.time()
for i, result in enumerate(scidir):
    if i == 0 and old is not None:
        index, list_raw_data = old

    if i < index:
        continue
    print(i)
    if i%50 == 0 and i != 0:
        pickle.dump([i, list_raw_data], open("scidir_metadata.p", "wb"))
        pickle.dump([i, list_raw_data], open("backup/scidir_metadata_" + str(i) + ".p", "wb"))
        print("time to get 50: {} minutes".format((time.time() - range_time) / 60))
        print("Total time remaining: {} hours".format((((len(scidir) - i) / 50) * (time.time() - range_time)) / 3600))
        range_time = time.time()

    try:
        ## scidir (Abtract) document example
        # Initialize document with ID as integer
        doi_doc = FullDoc(doi = result["prism:doi"])
        if doi_doc.read(client):
            list_raw_data.append(doi_doc)
        else:
            print ("Read document failed.")
    except Exception as e:
        print(e)
        continue
