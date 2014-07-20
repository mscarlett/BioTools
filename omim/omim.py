"""
Copyright 2014 Michael Scarlett

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

"""Provides code to access the OMIM API. 

For information about using the OMIM API and a description of keywords, please visit the following web page:
http://www.omim.org/help/api

To use the API you must include your API key with every request. If you do not
already have an API key then you can register for one by visiting http://www.omim.org/api.

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
_requireParameter    Internal function to check if a required parameter is included in the keywords
"""

import time
import urllib
import urllib2
import warnings

#There are two API hosts available, one located in the United States:
US_API_HOST = "http://api.omim.org"
#and the other located in Europe:
EU_API_HOST = "http://api.europe.omim.org"
#By default apiHost is set to US_API_HOST, but you should change it to EU_API_HOST if that server is closer.
apiHost = US_API_HOST

def entry(**keywords):
    """Fetches OMIM entry results which are returned as a file handle-like object. 
    
    'mimNumber' is required to be among the keywords.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    _requireParameter("mimNumber", keywords)
        
    handler = "entry"
    response = _fetch(apiHost, handler, **keywords)
    return response

def clinicalSynopsis(**keywords):
    """Fetches OMIM clinical synopsis results which are returned as a file handle-like object.
    
    'mimNumber' is required to be among the keywords.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    _requireParameter("mimNumber", keywords)
    
    handler = "clinicalSynopsis"
    response = _fetch(apiHost, handler, **keywords)
    return response

def search(handler = "entry", **keywords):
    """Fetches OMIM search results which are returned as a file handle-like object.
    
    'search' is required to be among the keywords.
    
    handler - the handler refers to the data object to search for. By default handler is set to
    'entry', but other possible values are 'geneMap' and 'clinicalSynopsis'.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    _requireParameter("search", keywords)
    
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

def allelicVariantList(**keywords):
    """Fetches OMIM allelic variant list for particular MIM entries which is returned as a file handle-like object. 
    
    'mimNumber' is required to be among the keywords.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    _requireParameter("mimNumber", keywords)
    
    handler = "entry/allelicVariantList"
    response = _fetch(apiHost, handler, **keywords)
    return response

def referenceList(**keywords):
    """Fetches OMIM reference list for particular MIM entries which is returned as a file handle-like object.
    
    'mimNumber' is required to be among the keywords.
    
    See the online documentation for an explanation of parameters:
    http://www.omim.org/help/api
    """
    _requireParameter("mimNumber", keywords)
    
    handler = "entry/referenceList"
    response = _fetch(apiHost, handler, **keywords)
    return response

def _fetch(domain, handler, **params):
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
    #Make sure API key is defined   
    _requireParameter("apiKey", params,
        """
        API key is not specified. OMIM requires you to include it with every request.
        If you do not have an API key, then visit http://www.omim.org/api to register for one.
        """)
    #Build the url and generate HTTP request
    query = urllib.urlencode(params)
    url = "%s/api/%s/?%s" % (domain, handler, query)
    req = urllib2.Request(url)
    # Return response as file-like object
    response = urllib2.urlopen(req)
    return response
    
_fetch.previous = 0

def _requireParameter(parameter, _dict, message = None):
    """ Helper function that checks if a given parameter is in the dictionary.
    A warning is given if the key cannot be found.
    """
    try:
        _dict[parameter]
    except KeyError:
        if message == None:
            message = "Required parameter '%s' is not specified" % parameter
        warnings.warn(message, UserWarning)