import requests

url = "https://nefitarif-io.onrender.com/admin/import"
headers = {"X-Admin-Token": "devtoken"}

resp = requests.post(url, headers=headers, json={})
print("Status:", resp.status_code)
print("Response:", resp.text)
