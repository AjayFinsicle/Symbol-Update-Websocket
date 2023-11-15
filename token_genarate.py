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
    "refresh_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MDAwMjI4MzEsImV4cCI6MTcwMTMwNDI1MSwibmJmIjoxNzAwMDIyODMxLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6InJlZnJlc2hfdG9rZW4iLCJhdF9oYXNoIjoiZ0FBQUFBQmxWRW92aG8tdzdibEc0aFc0Yld4WmRrVDVSUzlCaHZSZnJmeWhlMnZTN29yWXJSU3ExR1JSUjc4ZldMUWwzM216YVF0aW5NaURlTTFYRXVSdDFTcHZOTkJGaUJIZzdUR3o5ekk0cWw2Y2s1MkFNUmc9IiwiZGlzcGxheV9uYW1lIjoiRklOU0lDTEUgUFJJVkFURSBMSU1JVEVEIiwib21zIjoiSzEiLCJoc21fa2V5IjoiODhhNjc1MGI3OGZjYjViNjRmYTllZWU0NjU5ZGU1ZGQxYWNjNDFhZjcyYjlmZTVlNTAwYWE4NDciLCJmeV9pZCI6IkNBMDAxMzgiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.vdFkqWbajCGLOa0HT0mbU1roh68vRsqBJ3qsDQEcoE4",
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
