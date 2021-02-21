from app import flaskapp
from flask import request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from unidecode import unidecode

#@flaskapp.route('/', methods=['GET'])
@flaskapp.route('/bot', methods=['POST'])
def bot():
    request_msg = unidecode(request.values.get('Body', '').lower()) #remove acentos

    #response
    response = MessagingResponse()
    response_msg = response.message()

    responded = False
    if 'citacao' in request_msg:
        headers = {
            'content-type' : 'application/json'
            #'X-TheySaidSo-Api-Secret' : 'buibui10'
        }

        citacao_resp = requests.get('https://api.quotable.io/random', headers=headers)
        #print(citacao_resp)

        if citacao_resp.status_code == 200:
            data = citacao_resp.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Não foi possivel recuperar uma citacao neste momento.', 400
        response_msg.body(quote)
        responded = True

    if 'gato' in request_msg or 'gata' in request_msg:
        response_msg.media('https://cataas.com/cat')
        responded = True

    if 'star wars' in request_msg:
        response_msg.body('Que a força esteja com você! :D')
        responded = True

    if not responded:
        response_msg.body('Só conheço frases e gatos famosos! =/')

    return str(response), 200