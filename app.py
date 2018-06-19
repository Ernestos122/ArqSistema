from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests

#enviroment variables
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), './.env')
load_dotenv(dotenv_path)

KEY2    = environ.get('KEY2')
URL_API = environ.get('URL_API')
KEY4    = environ.get('KEY4')
URL_API2 = environ.get('URL_API2')


app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def inicio():
    return jsonify(
            status = 200
           )
@app.route('/visual', methods = ['POST', 'GET'])
def visual():
    if request.method == 'POST':
        url = URL_API

        querystring = {"maxCandidates":"1"}

        payload = "{\"url\":\"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgcMnNNsvae8dK-yMySErig229IzAV2dzIiGrH-YEfPXmzZaa0DQ\"}"
        headers = {
            'Content-Type': "application/json",
            'Ocp-Apim-Subscription-Key': KEY2,
            'Cache-Control': "no-cache",
            'Postman-Token': "a77b2af8-05c4-160b-a138-5b8d610428fa"
            }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        print(response.text)
        return jsonify(
            status = response.text
           )
    else:
        return jsonify(
            message = 'send the parameters'
           )

    
@app.route('/text', methods = ['POST', 'GET'])
def text():
    if request.method == 'POST':
        url = URL_API2
        payload = "{'documents': [{'id':'1', 'text':'hola'}]}"
        
        headers = {
            'Content-Type': "application/json",
            'Ocp-Apim-Subscription-Key': KEY4,
            'Cache-Control': "no-cache",
            'Postman-Token': "c21a5c6c-cefe-e4f6-8e37-12ad8c89319c"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        return jsonify(
            status = response.text
           )

    else:
        return jsonify(
            message = 'send the parameters'
           )
 
    
@app.route('/send_data_db', methods = ['POST', 'GET'])
def send_data_db():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True , port = 5000)
