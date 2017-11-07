"""An example program that uses the elsapy module"""

from elsapy.elsapy.elsclient import ElsClient
from elsapy.elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elsapy.elssearch import ElsSearch
import json
import pickle

## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])

## Initialize doc search object and execute search, retrieving all results
doc_srch = ElsSearch('artificial+intelligence','scopus')
import time
print("starting execute", doc_srch.index)
start_time = time.time()
print(doc_srch.execute(client, get_all = True))
print("scopus time:	", time.time() - start_time)
print("storing data..")

pickle.dump(doc_srch, open("scopus_result.p", "wb"))

doc_srch = ElsSearch('artificial+intelligence','scidir')
print("starting execute", doc_srch.index)
print(doc_srch.execute(client, get_all = True))
print("storing data..")

pickle.dump(doc_srch, open("scidir_result.p", "wb"))