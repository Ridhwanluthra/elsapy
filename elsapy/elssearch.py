"""The search module of elsapy.
    Additional resources:
    * https://github.com/ElsevierDev/elsapy
    * https://dev.elsevier.com
    * https://api.elsevier.com"""

from . import log_util

logger = log_util.get_logger(__name__)

class ElsSearch():
    """Represents a search to one of the search indexes accessible
         through api.elsevier.com. Returns True if successful; else, False."""

    # static variables
    __base_url = u'https://api.elsevier.com/content/search/'

    def __init__(self, query, index):
        """Initializes a search object with a query and target index."""
        self.query = query
        self.index = index
        self._uri = self.__base_url + self.index + '?query=' + self.query

    # properties
    @property
    def query(self):
        """Gets the search query"""
        return self._query

    @query.setter
    def query(self, query):
        """Sets the search query"""
        self._query = query

    @property
    def index(self):
        """Gets the label of the index targeted by the search"""
        return self._index

    @index.setter
    def index(self, index):
        self._index = index
        """Sets the label of the index targeted by the search"""

    @property
    def results(self):
        """Gets the results for the search"""
        return self._results

    @property
    def tot_num_res(self):
        """Gets the total number of results that exist in the index for
            this query. This number might be larger than can be retrieved
            and stored in a single ElsSearch object (i.e. 5,000)."""
        return self._tot_num_res

    @property
    def num_res(self):
        """Gets the number of results for this query that are stored in the 
            search object. This number might be smaller than the number of 
            results that exist in the index for the query."""
        return len(self.results)

    @property
    def uri(self):
        """Gets the request uri for the search"""
        return self._uri

    def execute(self, els_client=None, get_all=False, num_results=100):
        """Executes the search. If get_all = False (default), this retrieves
            the default number of results specified for the API. If
            get_all = True, multiple API calls will be made to iteratively get 
            all results for the search, up to a maximum of 5,000."""
        ## TODO: add exception handling
        api_response = els_client.exec_request(self._uri)
        self._tot_num_res = int(api_response['search-results']['opensearch:totalResults'])
        print(self._tot_num_res)
        self._results = api_response['search-results']['entry']
        if get_all is True:
            import time
            import pickle
            i = 1
            range_time = time.time()
            while (self.num_res < self.tot_num_res):
                try:
                    if i%50 == 0:
                        # store into pickle files
                        pickle.dump([i, api_response, self._results], open("scidir_search_results.p", "wb"))
                        pickle.dump([i, api_response, self._results], open("backup/scidir_search_results_" + str(i) + ".p", "wb"))
                        
                        print("time to get 50: {} minutes".format((time.time() - range_time) / 60))
                        print("Total time remaining: {} hours".format(((((self.tot_num_res / 25) - i) / 50) * (time.time() - range_time)) / 3600))
                        
                        range_time = time.time()
                    
                    print("{}: {}% done".format(i, (self.num_res / self.tot_num_res) * 100))
                    
                    for e in api_response['search-results']['link']:
                        if e['@ref'] == 'next':
                            next_url = e['@href']
                    
                    api_response = els_client.exec_request(next_url)
                    self._results += api_response['search-results']['entry']
                    i+=1
                except Exception as e:
                    print(e)
                    continue

    def hasAllResults(self):
        """Returns true if the search object has retrieved all results for the
            query from the index (i.e. num_res equals tot_num_res)."""
        return (self.num_res is self.tot_num_res)
