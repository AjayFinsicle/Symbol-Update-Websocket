import requests
import hashlib



APPID = "8UODZT9W8O-100"
SECRECTKEY = "Y9PGXWX048"
data_to_hash = APPID + SECRECTKEY
sha256_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
# print(sha256_hash)
app_id_hash = sha256_hash

url = "https://api.fyers.in/api/v2/validate-refresh-token"
headers = {
    "Content-Type": "application/json"
}
data = {
    "grant_type": "refresh_token",
    "appIdHash": app_id_hash,
    # "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTY0MDUxNzgsImV4cCI6MTY5NzY3NTQzOCwibmJmIjoxNjk2NDA1MTc4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6InJlZnJlc2hfdG9rZW4iLCJhdF9oYXNoIjoiZ0FBQUFBQmxIUmE2aXJEUm5XZ3dZeEhiWE9xS0FnbExtTm96NlFWQXlBRGs2NjVmSnU2S3FIMG1wWks5WV8yTTNzY25ycHBmVVJORmVyeThINmpMa0pjNkR5emEtaUtPVS1VS1hvRm9pVU1ZOFNVX19uYjRmQWM9IiwiZGlzcGxheV9uYW1lIjoiRklOU0lDTEUgUFJJVkFURSBMSU1JVEVEIiwib21zIjoiSzEiLCJoc21fa2V5IjoiODhhNjc1MGI3OGZjYjViNjRmYTllZWU0NjU5ZGU1ZGQxYWNjNDFhZjcyYjlmZTVlNTAwYWE4NDciLCJmeV9pZCI6IkNBMDAxMzgiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.pTDHManA5nLHp0_2waP33y9K6RK1yOvLAwhz4I6GJuo",
    "refresh_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTg2NDA3MTMsImV4cCI6MTY5OTkyMTgzMywibmJmIjoxNjk4NjQwNzEzLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6InJlZnJlc2hfdG9rZW4iLCJhdF9oYXNoIjoiZ0FBQUFBQmxQek5Ka0JRSHFnMkhNN3pBRk8tUzIzcTlRM0FVVUNvclNyX010OWJUNWhFS0xGU29hOWUwMFJWNkE5SlVmel9WMzNFVFh6Zlh2U29uNlc3cklDUC1GeUpHZWdDV0VNU1lQS3RmYkhOU2lucDd1Q1U9IiwiZGlzcGxheV9uYW1lIjoiRklOU0lDTEUgUFJJVkFURSBMSU1JVEVEIiwib21zIjoiSzEiLCJoc21fa2V5IjoiODhhNjc1MGI3OGZjYjViNjRmYTllZWU0NjU5ZGU1ZGQxYWNjNDFhZjcyYjlmZTVlNTAwYWE4NDciLCJmeV9pZCI6IkNBMDAxMzgiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.z5repieAunixhqGml2sQbPeuuxCPEObdBPFCppW-2go",
    "pin": "2023"
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    response_data = response.json()
    access_token = response_data.get("access_token")
    print("Access Token:", access_token)
else:
    print("Request failed with status code:", response.status_code)
    print("Response content:", response.text)
