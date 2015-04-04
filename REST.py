import requests

#Constants
apiurl = "http://192.168.1.191:5000/api"
apikey = "D3C09432B9B14506B00DDE3392814D68"

uri = apiurl + "/printer"
headers = { 'Content-type': 'application/json', 'X-Api-Key': apikey }
r = requests.get(uri, headers=headers)
print(r)
#j = r.json()

#print(j)