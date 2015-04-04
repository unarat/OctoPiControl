import requests
import json
import time
import os
import sys
from threading import Thread
 
# update these for your environment
apiurl = "http://localhost:5000/api"
apikey = "YOURKEYHERE"
pidfile = "/tmp/staywarm.pid"
 
# thread
def run():
    while True:
        # get temps
        uri = apiurl + "/printer"
        headers = { 'Content-type': 'application/json', 'X-Api-Key': apikey }
        r = requests.get(uri, headers=headers)
 
        if r.status_code >= 400:
          print "Error: couldn't get temperature from API"
          return
 
        j = r.json()
 
        # set target temp if there is one
        if j['temps']['bed']['target'] is not None:
          uri = apiurl + "/printer/bed"
          body = { 'command': 'target', 'target': j['temps']['bed']['target'] }
          r = requests.post(uri, headers=headers, data=json.dumps(body))
 
        if j['temps']['tool0']['target'] is not None:
          uri = apiurl + "/printer/tool"
          body = { 'command': 'target', 'targets': { 'tool0': j['temps']['tool0']['target'] } }
          r = requests.post(uri, headers=headers, data=json.dumps(body))
 
        time.sleep(30)
 
def check_pid(pid):
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError):
        return False
    else:
        return True
 
# check if we are already running, stop and exit if so (turn off)
if os.path.isfile(pidfile):
  p = open(pidfile, "r")
  oldpid = p.readline()
  if check_pid(oldpid):
    print "Staywarm is running, killing it."
    os.kill(int(oldpid), 9)
    os.unlink(pidfile)
    sys.exit()
  os.unlink(pidfile)
 
# fork into the background and keep setting the temp every 30 seconds (turn on)
pid = os.fork()
if(pid == 0):
  os.chdir("/")
  os.setsid()
  os.umask(0)
  pid2 = os.fork()
  if(pid2 == 0):
    t = Thread(target=run, args=())
    t.start()
    mypid = os.getpid()
    print "Forked to child pid %d" % mypid
    f = file(pidfile, "w")
    f.write("%d" % mypid)
    f.close()
    sys.exit()
  else:
    sys.exit()
else:
  sys.exit()