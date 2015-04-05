import requests
import json

#Constants
#octopi
#apiurl = "http://192.168.1.191:5000/api"
#apikey = "D3C09432B9B14506B00DDE3392814D68"

#x60
apiurl = "http://192.168.1.200:5000/api"
apikey = "2AE19BC0BE0C4E7296B03325DF2C4489"

#uri = apiurl + "/printer?exclude=temperature,sd"
uri = apiurl + "/state"
headers = { 'Content-type': 'application/json', 'X-Api-Key': apikey }
r = requests.get(uri, headers=headers)
#print(r)
j = r.json()

#print(j['state']['stateString'])
print(j)

uri = apiurl + "/printer/printhead"
body = { 'command': 'home', 'axes': ["x","y"] }
r = requests.post(uri, headers=headers, data=json.dumps(body))