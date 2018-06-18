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

        querystring = {"maxCandidates":"1"} # para los params, recuerdo que esto te dejaba la mejor prediccion. dado que no puedo testear este codigo, no se si se mantendra lo mismo, o sera otra forma de presentar.
                #params = urllib.parse.urlencode({  }) esto es lo que sale en los ejemplos como params, pero nuevamente, sin testeo, lo deje como estaba
       documents = {'documents' : [
 	 {'id': '1', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
  	 {'id': '2', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'}
	]}  


 headers = {
            'Content-Type': "application/json",
            'Ocp-Apim-Subscription-Key': KEY4,
            'Cache-Control': "no-cache",
            'Postman-Token': "a77b2af8-05c4-160b-a138-5b8d610428fa" #En teoria, esto deberia estar bueno, si es que usa el mismo token desde Postman, pero no cacho.
            }

        response = requests.request("POST", url, data=documents, headers=headers, params=querystring)

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
