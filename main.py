from flask import Flask, request, jsonify
from azure.communication.email import EmailClient
import os
import json
from dotenv import load_dotenv


app = Flask(__name__) #Creacion de la app flask

@app.route('/send_data', methods=['POST']) #Decorador para la ruta de la API
def send_email(): #Funcion que enviara el email
    load_dotenv() #Carga de las variables de entorno
    try: 
        connection_string = os.getenv('connection_string')
        client = EmailClient.from_connection_string(connection_string) #Creacion del cliente de email   

        data = request.get_json() #Obtencion del mensaje a enviar
        subject = data['subject'] #Obtencion del asunto del email
        # body = message['body'] #Obtencion del cuerpo del email
        recipients = data['recipients'] #Obtencion de los destinatarios del email
        html_body = data['html_body'] #Obtencion del cuerpo del email en formato HTML
        

        send_message = {
            "senderAddress": os.getenv('send_email'), #Quien lo envia 
            "recipients": {
                "to": [{"address": recipients}] #A quien se envia
            },
            # address : "correo", 
            # address : "otro correo"
            #esto en postman
            
            "content": {
                "subject": subject, #Asunto
                "html": html_body #Cuerpo del email
            },
        }

        poller = client.begin_send(send_message) #Envio del email
        result = poller.result()
        return jsonify({'message': 'Mensaje enviado correctamente'}), 200
        # if result.status == 202:
        #     return jsonify({'message': 'Mensaje enviado correctamente'})   
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Error al enviar el mensaje'}), 400
    

if __name__ == '__main__':
    app.run(debug=True)
        
