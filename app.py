from flask import Flask, request, jsonify
import requests as requests
app = Flask(__name__)

# Config
version = "v13.0"
phoneNumberId = "" # Your phone Number Id
urlMessageTextSend = f"https://graph.facebook.com/{version}/{phoneNumberId}/messages"
bearerToken = "" # Your authorization bearer token here
authorizationBearerToken = "Bearer "+ bearerToken

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        print("Received a message !")
        # Read receipt.
        readReceipt(request.json)
        
        try:
            recipientNumber = getFromNumber(request.json)
            requests.post(urlMessageTextSend,json=
                {
                    "messaging_product": "whatsapp",
                    "preview_url": False,
                    "recipient_type": "individual",
                    "to": recipientNumber,
                    "type": "text",
                    "text": {
                        "body": "Hello World"
                    }
                }, headers={"Authorization":authorizationBearerToken}
            )
            print("Message Succesfully Read ")
        except:
            print("Error Occurred Reading")        
        return ''
    elif request.method == 'GET':
        return request.args['hub.challenge']

    

def getFromNumber(msgJson):
    return msgJson["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

def getMessageText(msgJson):
    return msgJson["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

def readReceipt(msg):
    try:
        for message in msg['entry'][0]['changes'][0]['value']['messages']:
            messageId = message['id']
            print(f"Sending Message as Read {messageId}")
            resp = requests.post(urlMessageTextSend,
             {
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": messageId
            },headers={"Authorization":authorizationBearerToken}
            )
            print("Message Succesfully Read")
    except:
        print("Error Occurred Reading")

if(__name__) == '__main__':
    app.run()
