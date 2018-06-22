from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests
import os
import uuid
import csv
import ast
import json
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

@app.route('/process', methods = ['POST', 'GET'])
def process():
    data = None
    if request.method == 'POST':
        feature_vector = {
            "mountain":"50",
            "young": "10",
        }
        with open("image/input/1.txt", "r") as data_image:
            image = data_image.readlines()
            image_caption = []
            for img in image:
                
                url = "http://0.0.0.0:5000/visual"

                img = img.split("\n")
                payload = "{'url':'"+img[0]+"'}"
                payload = str(payload).strip("'<>() ").replace('\'', '\"')
                #print(payload)
                headers = {
                    'Content-Type': "application/json",
                    'Ocp-Apim-Subscription-Key': "4703fab05e7c4616915ee6c3aaebfa5d",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "cf316d57-4414-2a56-eaa1-910b0ea418eb"
                    }

                response = requests.request("POST", url, data=payload, headers=headers)
                data_output = response.json()
                image_caption.append(data_output['status']['description']['captions'][0]['text'])
            #print(image_caption[0])#esta data va a luis
        data_image.close()
        cont = 0
        image_features = []
        for i in image_caption:
            text_image = str(image_caption[cont])
            text_image = text_image.split("\n")    
            url2 = "http://0.0.0.0:5000/luis"

            #payload2 = "{\"text\":\"a man riding a wave on a surfboard in the water\"}"
            payload2 = "{'text':'"+text_image[0]+"'}"
            payload2 = str(payload2).strip("'<>() ").replace('\'', '\"')
            headers2 = {
                'Content-Type': "application/json",
                'Cache-Control': "no-cache",
                'Postman-Token': "858dd77b-dd8a-b33c-002a-3927dbc03f08"
                }

            response2 = requests.request("POST", url2, data=payload2, headers=headers2)
            data_output = response2.json()
            image_features.append(data_output['status']['topScoringIntent']['intent'])
            cont = cont + 1
        return jsonify(
            data = image_features
           )
    else:
        return jsonify(
            message = 'send the parameters'
           )

@app.route('/visual', methods = ['POST', 'GET'])
def visual():
    data = None
    if request.method == 'POST':
        data = request.json
        if 'url' not in request.json.keys():
            return jsonify({"message" : "json missing 'url'."})
        image = data['url']
        url = URL_API
        querystring = {"maxCandidates":"1",
                       "language": "en"
                        }

        payload = "{'url':'"+image+"'}"
        headers = {
            'Content-Type': "application/json",
            'Ocp-Apim-Subscription-Key': KEY2,
            'Cache-Control': "no-cache",
            'Postman-Token': "a77b2af8-05c4-160b-a138-5b8d610428fa"
            }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        print(response.text)
        return jsonify(
            status = response.json()
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
            r = requests.get('	https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/221b5e66-c479-4b90-ab6b-03371e5bb456',headers=headers, params=params)
            print(r.json())

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        return jsonify(
            status = r.json()
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
