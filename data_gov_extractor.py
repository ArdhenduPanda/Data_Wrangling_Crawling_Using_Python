import os, sys
import urllib.request

try:
    print('Beginning file download with urllib2...')
    url = "https://data.gov.in/node/6264541/download"
    urllib.request.urlretrieve(url, 'C:/Users/ardhendupanda/Downloads/data_gov.csv')  
except:
	print "\nERROR: Please specify valid filename and url column name to download\n"	
	sys.exit(0)	
	
	
