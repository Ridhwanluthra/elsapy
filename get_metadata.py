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

scopus = pickle.load(open("scopus_results.p", "rb"))

list_raw_data = list()
index = 0

import os
if "scopus_metadata.p" in os.listdir():
    old = pickle.load(open("scopus_metadata.p", "rb"))
else:
    old = None

import time
range_time = time.time()
for i, result in enumerate(scopus.results):
    if i == 0 and old is not None:
        index, list_raw_data = old

    if i < index:
        continue
    print(i)
    if i%50 == 0 and i != 0:
        pickle.dump([i, list_raw_data], open("scopus_metadata.p", "wb"))
        pickle.dump([i, list_raw_data], open("backup/scopus_metadata_" + str(i) + ".p", "wb"))
        print("time to get 50: {} minutes".format((time.time() - range_time) / 60))
        print("Total time remaining: {} hours".format((((len(scopus.results) - i) / 50) * (time.time() - range_time)) / 3600))
        range_time = time.time()

    try:
        int_id = int(result["dc:identifier"][10:])

        ## Scopus (Abtract) document example
        # Initialize document with ID as integer
        scp_doc = AbsDoc(scp_id = int_id)
        if scp_doc.read(client):
            # print ("scp_doc.title: ", scp_doc.title)
            list_raw_data.append(scp_doc)
        else:
            pickle.dump([i-1, list_raw_data], open("backup/scopus_metadata_" + i-1 + ".p", "wb"))
            print ("Read document failed.")
    except KeyboardInterrupt:
        pickle.dump([i-1, list_raw_data], open("scopus_metadata.p", "wb"))
        break
    except Exception as e:
        print(e)
        continue

pickle.dump([i, list_raw_data], open("scopus_metadata.p", "wb"))
# ## ScienceDirect (full-text) document example using DOI
# doi_doc = FullDoc(doi = '10.1016/S1525-1578(10)60571-5')
# if doi_doc.read(client):
#     print ("doi_doc.title: ", doi_doc.title)
#     doi_doc.write()   
# else:
#     print ("Read document failed.")