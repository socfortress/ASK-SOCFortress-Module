#!/var/ossec/framework/python/bin/python3
# Copyright (C) 2023, SOCFortress, LLP.
import json
import sys
import time
import os
import ipaddress
import re
from socket import socket, AF_UNIX, SOCK_DGRAM
try:
    import requests
    from requests.auth import HTTPBasicAuth
except Exception as e:
    print("No module 'requests' found. Install: pip install requests")
    sys.exit(1)
# Global vars
debug_enabled = False
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
json_alert = {}
now = time.strftime("%a %b %d %H:%M:%S %Z %Y")
# Set paths
log_file = '{0}/logs/integrations.log'.format(pwd)
socket_addr = '{0}/queue/sockets/queue'.format(pwd)
def main(args):
    debug("# Starting")
    # Read args
    alert_file_location = args[1]
    apikey = args[2]
    debug("# API Key")
    debug(apikey)
    debug("# File location")
    debug(alert_file_location)
    # Load alert. Parse JSON object.
    with open(alert_file_location) as alert_file:
        json_alert = json.load(alert_file)
    debug("# Processing alert")
    debug(json_alert)
    # Request SOCFortress info
    msg = request_socfortress_api(json_alert,apikey)
    # If positive match, send event to Wazuh Manager
    if msg:
        send_event(msg, json_alert["agent"])

def debug(msg):
    if debug_enabled:
        msg = "{0}: {1}\n".format(now, msg)
        print(msg)
        f = open(log_file,"a")
        f.write(msg)
        f.close()

def query_api(sigma_name, apikey, product):
  params = {'name': sigma_name,}
  headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  "x-api-key": apikey,
  "module-version": "1.0",
  "product": product,
  }
  response = requests.get('https://api.socfortress.co/v1/sigma', params=params, headers=headers)
  if response.status_code == 200:
      json_response = response.json()
      data = json_response.get('message')
      return data
  elif response.status_code == 403 or response.status_code == 429:
      json_response = response.json()
      data = json_response
      alert_output = {}
      alert_output["socfortress"] = {}
      alert_output["integration"] = "custom-socfortress-knowledgebase"
      alert_output["socfortress"]["status_code"] = response.status_code
      alert_output["socfortress"]["message"] = json_response['message']
      send_event(alert_output)
      exit(0)
  else:
      alert_output = {}
      alert_output["socfortress"] = {}
      alert_output["integration"] = "custom-socfortress-knowledgebase"
      json_response = response.json()
      debug("# Error: The SOCFortress integration encountered an error")
      alert_output["socfortress"]["status_code"] = response.status_code
      alert_output["socfortress"]["message"] = json_response['error']
      send_event(alert_output)
      exit(0)

def request_socfortress_api(alert, apikey):
    alert_output = {}
    # Collect the SIGMA Rule Name - Currently only Supports Chainsaw for Windows
    event_source = alert["rule"]["groups"][0]
    if 'chainsaw' in event_source.lower():
        if 'name' in alert["data"]:
            ## URL encode where a space is present
            sigma_rule = alert["data"]["name"].replace(" ", "%20")
            product = 'windows'
            data = query_api(sigma_rule, apikey, product)
        else:
            return(0)
    else:
        return(0)
    # Create alert
    alert_output["socfortress"] = {}
    alert_output["integration"] = "custom-socfortress"
    alert_output["socfortress"]["found"] = 0
    alert_output["socfortress"]["source"] = {}
    alert_output["socfortress"]["source"]["alert_id"] = alert["id"]
    alert_output["socfortress"]["source"]["agent_name"] = alert["agent"]["name"]
    alert_output["socfortress"]["source"]["rule"] = alert["rule"]["id"]
    alert_output["socfortress"]["source"]["description"] = alert["rule"]["description"]
    alert_output["socfortress"]["source"]["processGuid"] = alert["data"]["win"]["eventdata"]["processGuid"]
    alert_output["socfortress"]["source"]["sigma_name"] = alert["data"]["name"]
    data = data
    # Populate JSON Output with SOCFortress results
    alert_output["socfortress"]["message"] = data

    debug(alert_output)
    return(alert_output)

def send_event(msg, agent = None):
    if not agent or agent["id"] == "000":
        string = '1:socfortress:{0}'.format(json.dumps(msg))
    else:
        string = '1:[{0}] ({1}) {2}->socfortress:{3}'.format(agent["id"], agent["name"], agent["ip"] if "ip" in agent else "any", json.dumps(msg))
    debug(string)
    sock = socket(AF_UNIX, SOCK_DGRAM)
    sock.connect(socket_addr)
    sock.send(string.encode())
    sock.close()

if __name__ == "__main__":
    try:
        # Read arguments
        bad_arguments = False
        if len(sys.argv) >= 4:
            msg = '{0} {1} {2} {3} {4}'.format(now, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else '')
            debug_enabled = (len(sys.argv) > 4 and sys.argv[4] == 'debug')
        else:
            msg = '{0} Wrong arguments'.format(now)
            bad_arguments = True
        # Logging the call
        f = open(log_file, 'a')
        f.write(msg +'\n')
        f.close()
        if bad_arguments:
            debug("# Exiting: Bad arguments.")
            sys.exit(1)
        # Main function
        main(sys.argv)
    except Exception as e:
        debug(str(e))
        raise