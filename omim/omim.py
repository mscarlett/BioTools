"""
Copyright 2014 Michael Scarlett

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

"""Provides code to access the OMIM API. 

For information about using the OMIM API and a description of keywords, please visit the following web page:
http://www.omim.org/help/api

To use the functions in this module, include the OMIM API keywords as input parameters.

IMPORTANT: To use the API you must include your API key with every request. If you do not
already have an API key then you can register for one by visiting http://www.omim.org/api.

For example if your API key is XXXXXXXXXX then you would include it as one of your
function parameters and can query OMIM entry number 141900 by specifying:
>> response = omim.entry(mimNumber="141900", apiKey="XXXXXXXXXX")

Note that each function returns results as a file-handle like object which you can either
iterate over:
>> for line in response:
>>     print line
or you can read at once.
>> results = response.read()

Variables:
US_API_HOST          The subdomain of the United States API host
EU_API_HOST          The subdomain of the Europe API host
apiHost              The name of the API host to use, which determines whether to use US_API_HOST or EU_API_HOST

Functions:
entry                Retrieves records in the requested format by MIM number
clinicalSynopsis     Retries the clinical annotation associated with the MIM number
searchGeneMap        Searches the OMIM gene map
allelicVariantList   Retrieves a list of allelic variants associated with the MIM number
referenceList        Retrieves a list of references associated with the MIM number
_fetch               Internal function used to send the HTTP request to OMIM and return a response
"""

import time
import urllib
import urllib2

#There are two API hosts available, one located in the United States:
US_API_HOST = "http://api.omim.org"
#and the other located in Europe:
EU_API_HOST = "http://api.europe.omim.org"
#By default apiHost is set to US_API_HOST, but change it to EU_API_HOST if that server is closer.
apiHost = US_API_HOST

def entry(mimNumber, **keywords):
    """Fetches OMIM entry results which are returned as a file handle-like object.
    
    'mimNumber' is required to be among the parameters.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    keywords["mimNumber"] = mimNumber
    handler = "entry"
    response = _fetch(apiHost, handler, **keywords)
    return response

def clinicalSynopsis(mimNumber, **keywords):
    """Fetches OMIM clinical synopsis results which are returned as a file handle-like object.
    
    'mimNumber' is required to be among the parameters.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    keywords["mimNumber"] = mimNumber
    handler = "clinicalSynopsis"
    response = _fetch(apiHost, handler, **keywords)
    return response

def search(search, handler = "entry", **keywords):
    """Fetches OMIM search results which are returned as a file handle-like object.
    
    'search' is required to be among the parameters.
    
    handler - the handler refers to the data object to search for. By default handler is set to
    'entry', but other possible values are 'geneMap' and 'clinicalSynopsis'.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    keywords["search"] = search
    handler = "search/" + handler
    response = _fetch(apiHost, handler, **keywords)
    return response

def geneMap(**keywords):
    """Fetches OMIM gene map results which are returned as a handle. 
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    
    Note that OMIM enforces a limit of 100 gene map entries per request.
    """
    handler = "genemap"
    response = _fetch(apiHost, handler, **keywords)
    return response

def allelicVariantList(mimNumber, **keywords):
    """Fetches OMIM allelic variant list for particular MIM entries which is returned as a file handle-like object. 
    
    'mimNumber' is required to be among the parameters.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    keywords["mimNumber"] = mimNumber
    handler = "entry/allelicVariantList"
    response = _fetch(apiHost, handler, **keywords)
    return response

def referenceList(mimNumber, **keywords):
    """Fetches OMIM reference list for particular MIM entries which is returned as a file handle-like object.
    
    'mimNumber' is required to be among the keywords.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    keywords["mimNumber"] = mimNumber
    handler = "entry/referenceList"
    response = _fetch(apiHost, handler, **keywords)
    return response

def _fetch(baseurl, handler, **keywords):
    """Helper function to build the URL and open a handle to it.
     
    Opens a handle to OMIM using the URL path and parameters.
    
    This function also enforces the "up to four queries per second rule" 
    in accordance with the OMIM API policy. As a result there is a minimum
    delay of 0.25 seconds between requests.
    """ 
    #Enforce the "up to four queries per second rule" with a 0.25 second delay
    current = time.time()
    wait = _fetch.previous + 0.25 - current
    if wait > 0:
        time.sleep(wait)
        _fetch.previous = current + wait 
    else:
        _fetch.previous = current
    #Build the url and generate HTTP request
    query = urllib.urlencode(keywords)
    url = "%s/api/%s/?%s" % (baseurl, handler, query)
    request = urllib2.Request(url)
    # Return response as file-like object
    response = urllib2.urlopen(request)
    return response
    
_fetch.previous = 0