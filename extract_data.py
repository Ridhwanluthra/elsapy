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

# def coredata_extraction(data, raw_data):
# 	raw_data["doi"] = data["prism:doi"]
# 	raw_data["type"] = data["prism:aggregationType"]
# 	raw_data["title"] = data["dc:title"]
# 	raw_data["cite_count"] = data["citedby-count"]
# 	raw_data["publication_name"] = data["prism:publicationName"]
# 	raw_data["volume"] = data["prism:volume"]
# 	raw_data["issue_num"] = data["prism:issueIdentifier"]
# 	raw_data["start_end_page"] = [data["prism:startingPage"], data["prism:endingPage"]]
# 	raw_data["cover_date"] = data["prism:coverDate"]

# 	raw_data["authors"] = []
# 	for name in data["dc:creator"]["author"]:
# 		raw_data["authors"].append(name["ce:indexed-name"])

# 	raw_data["abstract"] = data["dc:description"]

# 	return raw_data

# def bibdata_extraction(data, raw_data):
# 	raw_data["reference_count"] = data["@refcount"]
# 	raw_data[]

# def extract_data_scopus(data):
# 	raw_data = dict()
# 	raw_data = coredata_extraction(data["coredata"], raw_data)
# 	raw_data["keywords"] = data["authkeywords"]

# 	raw_data["subject_area"] = []
# 	for area in data["subject-areas"]["subject-area"]:
# 		raw_data["subject_area"].append(area["$"])

# 	raw_data = bibdata_extraction(data["item"]["bibrecord"]["tail"]["bibliography"], raw_data)


for i, result in enumerate(scopus.results):
	print(i)
	try:
		int_id = int(result["dc:identifier"][10:])

		## Scopus (Abtract) document example
		# Initialize document with ID as integer
		scp_doc = AbsDoc(scp_id = int_id)
		if scp_doc.read(client):
		    print ("scp_doc.title: ", scp_doc.title)
		    list_raw_data.append(scp_doc)
		else:
		    print ("Read document failed.")
	except:
		continue

pickle.dump(list_raw_data, open("scopus_result_expanded.p", "wb"))
# ## ScienceDirect (full-text) document example using DOI
# doi_doc = FullDoc(doi = '10.1016/S1525-1578(10)60571-5')
# if doi_doc.read(client):
#     print ("doi_doc.title: ", doi_doc.title)
#     doi_doc.write()   
# else:
#     print ("Read document failed.")