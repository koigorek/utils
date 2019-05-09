#****************************************************************
"""
### THE BELOW TEXT IS OUTDATED and needs to be updated

#This replaces a previous version of gcard_helper.py by using the HTMLParser class
#This allows for more robust parsing of the html mother directory to find gcard files
#Even better would be to use BeautifulSoup, which would allow for the code to be condensed as:
#```import requests
#from bs4 import BeautifulSoup
#page = requests.get('http://www.website.com')
#bs = BeautifulSoup(page.content, features='lxml')
#for link in bs.findAll('a'):
#    print(link.get('href'))```
#Unfortunately, this module must be imported and cannot be gaurannted that it will be on whatever
#server this software will live on, so it is safer to instead use HTMLParser which is more common
####
#This file takes in a BatchID, unixtimestamp, and gcard url from db_batch_entry and passes it through
#a few functions to download the gcards from the specified location and to enter them into the
#appropriate gcard table in the database.
# Some effort should be developed to sanitize the gcard files to prevent
# against sql injection attacks
"""
#***************************************************************
from __future__ import print_function
import utils, file_struct, html_reader

def db_gcard_write(BatchID,timestamp,gcard_text):
    strn = "INSERT INTO Gcards(BatchID) VALUES ({0});".format(BatchID)
    utils.sql3_exec(strn)
    strn = """UPDATE Gcards SET {0} = "{1}" WHERE BatchID = {2};""".format('gcard_text',gcard_text,BatchID)
    utils.sql3_exec(strn)
    utils.printer("GCard added to database corresponding to BatchID {0}".format(BatchID))

def GCard_Entry(BatchID,unixtimestamp,url_dir):
  print("Gathering gcards from {0} ".format(url_dir))
  if url_dir == file_struct.gcard_default:
    utils.printer('Using gcard from /jlab/work')
    gcard_text_db = url_dir
    db_gcard_write(BatchID,unixtimestamp,gcard_text_db)
  elif 'https://' in url_dir:
    utils.printer('Trying to download gcards from online repository')
    raw_html, gcard_urls = html_reader.html_reader(url_dir,file_struct.gcard_identifying_text)
    for url_ending in gcard_urls:
      utils.printer('Gcard URL name is: '+url_ending)
      gcard_text = html_reader.html_reader(url_dir+'/'+url_ending,'')[0]#This returns a tuple, we need the contents of the tuple
      utils.printer2('HTML from gcard link is: {0}'.format(gcard_text))
      gcard_text_db = gcard_text.replace('"',"'")
      print("\t Gathered gcard '{0}'".format(url_ending))
      db_gcard_write(BatchID,unixtimestamp,gcard_text_db)
  else:
    print('gcard not recognized as default option or online repository, please inspect scard')
    exit()
