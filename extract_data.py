import pickle

list_raw_data = list()

def coredata_extraction(data, raw_data):
	try:
		raw_data["doi"] = data["prism:doi"]
		raw_data["type"] = data["prism:aggregationType"]
		raw_data["title"] = data["dc:title"]
		raw_data["cite_count"] = data["citedby-count"]
		raw_data["publication_name"] = data["prism:publicationName"]
		raw_data["volume"] = data["prism:volume"]
		# raw_data["issue_num"] = data["prism:issueIdentifier"]
		# raw_data["start_end_page"] = [data["prism:startingPage"], data["prism:endingPage"]]
		raw_data["cover_date"] = data["prism:coverDate"]

		raw_data["authors"] = []
		for name in data["dc:creator"]["author"]:
			raw_data["authors"].append(name["ce:indexed-name"])

	
		raw_data["abstract"] = data["dc:description"]
	except:
		return None

	return raw_data

def bibdata_extraction(data, raw_data):
	raw_data["reference_count"] = data["@refcount"]
	# raw_data[]
	return raw_data

def extract_data_scopus(data):
	raw_data = dict()
	raw_data = coredata_extraction(data["coredata"], raw_data)
	if raw_data is None:
		return None
	raw_data["keywords"] = data["authkeywords"]

	raw_data["subject_area"] = []
	for area in data["subject-areas"]["subject-area"]:
		raw_data["subject_area"].append(area["$"])

	try:
		raw_data = bibdata_extraction(data["item"]["bibrecord"]["tail"]["bibliography"], raw_data)
	except:
		return None

	return raw_data

if __name__ == "__main__":
	_, metadata = pickle.load(open("scopus_metadata.p", "rb"))
	for i in metadata:
		list_raw_data.append(extract_data_scopus(i.data))
	pickle.dump(list_raw_data, open("extracted_files/extracted_raw.p", "wb"))