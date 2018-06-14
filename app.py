import requests

url = "https://westus.api.cognitive.microsoft.com/vision/v1.0/describe"

querystring = {"maxCandidates":"1"}

payload = "{\"url\":\"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgcMnNNsvae8dK-yMySErig229IzAV2dzIiGrH-YEfPXmzZaa0DQ\"}"
headers = {
    'Content-Type': "application/json",
    'Ocp-Apim-Subscription-Key': "4703fab05e7c4616915ee6c3aaebfa5d",
    'Cache-Control': "no-cache",
    'Postman-Token': "a77b2af8-05c4-160b-a138-5b8d610428fa"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)