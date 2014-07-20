'''
Created on Jul 20, 2014

@author: Michael
'''
import urllib
import urllib2

formats = {"html", "tab", "xls", "fasta", "gff", "txt", "xml", "rdf", "list", "rss"}

def _fetch(url, format = "", **params):
    """Helper function to build the URL and open a handle to it.
     
    Open a handle to UniProt using the parameters.
    """
    data = urllib.urlencode(params)
    request = urllib2.Request(url + format, data)
    response = urllib2.urlopen(request)
    return response