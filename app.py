from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests
import os
import uuid
import csv
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
LUIS_KEY3 = environ.get('LUIS_KEY3')
LUIS_KEY1 = environ.get('LUIS_KEY1')
REGRESION = environ.get('REGRESION')


app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def inicio():
    return jsonify(
            status = 200
           )
@app.route('/visual', methods = ['POST', 'GET'])
def visual():
    data = None
    if request.method == 'POST':
        data = request.json
        if 'url' not in request.json.keys():
            return jsonify({"message" : "json missing 'url'."})
        images = data['url']
        url = URL_API
        with open(images,'r') as images:
            image = images.readlines()
            for img in image:    
                querystring = {"maxCandidates":"1",
                               "language": "en"
                                }

                payload = "{'url':'"+img+"'}"
                headers = {
                    'Content-Type': "application/json",
                    'Ocp-Apim-Subscription-Key': KEY2,
                    'Cache-Control': "no-cache",
                    'Postman-Token': "a77b2af8-05c4-160b-a138-5b8d610428fa"
                    }

                response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

                print(response.text)
        return jsonify(
            status = 200
            )
        
    else:
        return jsonify(
            message = 'send the parameters'
           )

    
@app.route('/text', methods = ['POST', 'GET'])
def text():
    data = None
    if request.method == 'POST':
        data = request.json
        if 'text' not in request.json.keys():
            return jsonify({"message" : "json missing 'text'."})
        text = data['text']
        url = URL_API2
        payload = "{'documents': [{'id':'1', 'text':'"+text+"'}]}"
        
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


@app.route('/luis', methods = ['POST', 'GET'])
def luis():
    data = None
    if request.method == 'POST':
        data = request.json
        if 'text' not in request.json.keys():
            return jsonify({"message" : "json missing 'text'."})
        text = data['text']
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': LUIS_KEY3,
        }

        params ={
            # Query parameter
            'q': text,
            'timezoneOffset': '0',
            'verbose': 'false',
            'spellCheck': 'false',
            'staging': 'false',
        }

        try:
            r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/10060bcf-803d-43a2-8611-a39275db7cea',headers=headers, params=params)
            print(r.json())

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        return jsonify(
            status = r.text
           )
    else:
        return jsonify(
            message = 'send the parameters'
           )

@app.route('/logistic', methods = ['POST', 'GET'])
def logistic():
    data = None
    if request.method == 'POST':
        #hay que crear un archivo unico con los parametros de la regresión
        #la salida debe ser unica
        #test set debe ser unico
        #el train set igual
        data = request.json
        if 'key' not in request.json.keys():
            return jsonify({"message" : "json missing 'key'."})
        if 'dataTestSet_url' not in request.json.keys():
            return jsonify({"message" : "json missing 'dataTestSet'."})
        if 'dataTrainSet_url' not in request.json.keys():
            return jsonify({"message" : "json missing 'dataTrainSet'."})
        if 'id' not in request.json.keys():
            return jsonify({"message" : "json missing 'thres'."})
        key              = data['key']
        dataTestSet_url  = str(data['dataTestSet_url'])
        dataTrainSet_url = str(data['dataTrainSet_url'])
        idus             = str(data['id'])
        temp             = 'regresion/temp.csv'
        with open(temp, 'w', newline='') as tmp:
            fieldnames = ['dataTestSet_url', 'dataTrainSet_url', 'id']
            writer = csv.DictWriter(tmp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'dataTestSet_url': dataTestSet_url, 'dataTrainSet_url': dataTrainSet_url, 'id': idus})

        if str(key) != 'clave':
            return jsonify({"message" : "bad key."})
        output_console = os.popen(REGRESION).readlines()
        print(output_console)
        return jsonify(
            status = 200
           ) 
    else:
        return jsonify(
            message = 'send the parameters'
           ) 

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True , port = 5000)
