"""
Copyright 2014 Michael Scarlett

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

"""Provides code to access UniProt programmatically.

For information about UniProt access and a description of keywords, please visit the following web page:
http://www.uniprot.org/faq/28

Variables:
URL                  The url to the UniProt website

Functions:
entry                Retrieve an entry from UniProt by identifier in the specified file format.
query                Search for an entry in the UniProt database.
mapping              Maps ids from one database to another.

_fetch               Internal function used to send the HTTP request to UniProt and return a response
"""
import urllib
import urllib2

#URL to the UniProt website
URL = "http://www.uniprot.org"

def entry(id, format = "", **keywords):
    """ Retrieve an individual entry from UniProt using the entry's unique id.
    
    You may also specify the format of the file to be retrieved. Accepted file formats
    are html, tab, xls, fasta, gff, txt, xml, rdf, list, and rss. By default an html page
    is returned if no format is specified.
    """
    dataset = "uniprot"
    response = _fetch(URL, dataset, id, format, **keywords)
    return response

def query(query, **keywords):
    """
    Search the UniProt database using a query.
    
    See http://www.uniprot.org/faq/28 for a description of parameters.
    """
    dataset = "uniprot"
    keywords["query"] = query
    response = _fetch(URL, dataset, **keywords)
    return response

def mapping(map_from, map_to, query, **keywords):
    """
    Map UniProt entries to those in other databases. To do this you will need to read
    http://www.uniprot.org/faq/28 for a list of database abbreviations.
    
    map_from : specify which database you wish to map identifiers from,
    map_to :   specify which database you wish to map identifiers to.
    query :    input all identifiers to map between databases as either a space delimited
               string or an iterable collection of strings.
    
    For example to get the OMIM ids for UniProt entries P13368, P20806, and Q9UM73 perform
    the following:
    >> query = "P13368 P20806 Q9UM73"
    >> response = mapping("ACC" ,"MIM_ID", query)
    >> response.read()
    
    See http://www.uniprot.org/faq/28 for more information.
    """
    #Databases to perform mapping between
    keywords["from"] = map_from
    keywords["to"] = map_to
    
    if hasattr(query, '__iter__'):
        query = " ".join(query)
    keywords["query"] = query
    
    dataset = "mapping"
    response = _fetch(URL, dataset, **keywords)
    return response

def _fetch(baseurl, dataset, id = "", format = "", **keywords):
    """Helper function to build the URL and open a handle to it.
     
    Open a handle to UniProt using the parameters.
    """
    #Check parameters    
    if format != "" and format[0] != ".":
        #Make sure there is an id
        if id == "":
            raise ValueError("id must be defined when format is defined.")
        #Append dot to format
        format = "%s." % format
        
    #Build the url and generate HTTP request
    data = urllib.urlencode(keywords)
    url = "%s/%s/%s%s" % (baseurl, dataset, id, format)
    request = urllib2.Request(url, data)
    #Add your email here to help in case of any problems.
    if "contact" in keywords:
        request.add_header('User-Agent', 'Python %s' % keywords["contact"])
    else:
        request.add_header('User-Agent', 'Python')
    # Return response as file-like object
    response = urllib2.urlopen(request)
    return response