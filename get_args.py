#****************************************************************
"""
# File Description
"""
#****************************************************************

from __future__ import print_function
import utils, file_struct
import sqlite3, argparse

def get_args():
  utils.printer2("Getting arguments from command line")
  argparser = argparse.ArgumentParser()
  argparser.add_argument('-b','--BatchID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
  argparser.add_argument('-t','--test', help = 'Use this flag (no arguments) if you are NOT on a farm node and want to test the submission flag (-s)', action = 'store_true')
  argparser.add_argument('-s','--submit', help = 'Use this flag (no arguments) if you want to submit the job', action = 'store_true')
  argparser.add_argument('scard',help = 'relative path and name scard you want to submit, e.g. ../scard.txt',nargs='?',)
  argparser.add_argument('-w','--write_files', help = 'Use this flag (no arguments) if you want submission files to be written out to text files', action = 'store_true')
  argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash, default = file_struct.debug_default,help = file_struct.debug_help)
  argparser.add_argument('-l','--lite',help = "use -l or --lite to connect to sqlite DB, otherwise use MySQL DB", action = 'store_true')
  args = argparser.parse_args()

  file_struct.DEBUG = getattr(args,file_struct.debug_long)
  file_struct.use_mysql = not args.lite

  if not args.lite:
    with open(file_struct.dirname+'/../msqlrw.txt','r') as myfile: #msql.txt is a file that contains two line: first line is username, second line is password
    #This is a temporary fix, need to store the password information outside of github
      login=myfile.read().replace('\n', ' ')
      login_params = login.split()
      file_struct.mysql_uname = login_params[0]
      file_struct.mysql_psswrd =  login_params[1]

  return args
