#!/usr/bin/env python
#import sys
import os
import logging
import pif
import pygodaddy
 
# GLOBALS
GODADDY_USERNAME=""
GODADDY_PASSWORD=""
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
  client = pygodaddy.GoDaddyClient()
  client.login(GODADDY_USERNAME, GODADDY_PASSWORD)
 
  for domain in client.find_domains():
    for dns_record in client.find_dns_records(domain):
      logging.debug("Domain '{0}' DNS records: {1}".format(domain, client.find_dns_records(domain)))
      # only update the bluewolf subdomain
      if dns_record.hostname == 'bluewolf':
        if public_ip != dns_record.value:
            if client.update_dns_record(dns_record.hostname+"."+domain, public_ip):
              logging.info("Host '{0}' public IP set to '{1}'".format(dns_record.hostname, public_ip))
              # update our local copy of IP
              write_ip_file()
              break
            else:
              logging.info("Failed to update Host '{0}' IP to '{1}'".format(dns_record.hostname, public_ip))
        else:
            logging.info("Nothing was changed")
            # We are 90% only here because there is no current_ip file. So, we write it now.
            write_ip_file()
      else:
        logging.info("Not Bluewolf: '{0}', skipping".format(dns_record.hostname))
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
public_ip = pif.get_public_ip()
 
if check_ip_file(public_ip) != 1:
  update_dns(public_ip)
