#!/usr/bin/env python
#import sys
import os
import logging
import pif
import godaddypy
 
# GLOBALS
GODADDY_USERNAME=""
GODADDY_PASSWORD=""
DOMAIN="" #something.com
# The files will be created automatically
LOGFILE='/SOME/PLACE/godaddy/godaddy.log'
IPFILE='/SOME/PLACE/godaddy/current_ip'
 
#
# check locally if IP has changed
#
def check_ip_file(public_ip):
  if os.path.exists(IPFILE):
    # Open a file
    fo = open(IPFILE, "r")
    old_ip = fo.read(50)
    fo.close()
    #print "Read String is : ", str
    # Close opend file
    if old_ip == public_ip:
      print "ip is the same.. not doing anything"
      return 1
  # return if no file exists, or the IP is new
  return
 
def write_ip_file():
  if not os.path.exists(IPFILE):
    fo = open(IPFILE, "w")
    fo.write(public_ip)
    fo.close()
  else:
    fo = open(IPFILE, "r+")
    fo.seek(0)
    fo.write(public_ip)
    fo.truncate()
    fo.close()
  return
 
def update_dns(public_ip):
  userAccount = godaddypy.Account(api_key=GODADDY_API_KEY, api_secret=GODADDY_API_SECRET)
  client = godaddypy.Client(userAccount)
 
  for domain in client.get_domains():
    if domain == DOMAIN:
        logging.debug("DOMAIN '{0}' found".format(DOMAIN))
        for dnsRecord in client.get_records(DOMAIN, record_type='A'):
            if public_ip != dnsRecord['data']:
                if client.update_record_ip(public_ip, DOMAIN, 'dynamic', 'A'):
                    logging.info("Host '{0}' public IP set to '{1}'".format(DOMAIN, public_ip))
                    write_ip_file()
                    break
                else:
                    logging.info("Failed to update Host '{0}' IP to '{1}'".format(DOMAIN, public_ip))
            else:
                logging.info("Nothing changed")
                write_ip_file()
  return
 
def constrain_logfile():
  # Don't allow the log file to become greater than 10MB
  if os.path.exists(LOGFILE):
    statinfo = os.stat(LOGFILE)
    if statinfo.st_size >= 10485760:
      print "removing log file"
      os.remove(LOGFILE)
  return
 
def setup_logfile():
  constrain_logfile()
  logging.basicConfig(filename=LOGFILE, format='%(asctime)s %(message)s', level=logging.INFO)
  return
 
### BEGIN MAIN PROCEDURE
setup_logfile()
public_ip = pif.get_public_ip('ident.me')
logging.debug("public_ip is '{0}'".format(public_ip))
 
if check_ip_file(public_ip) != 1:
  update_dns(public_ip)
