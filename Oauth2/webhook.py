from flask import Flask, request, render_template
from urllib.parse import urlencode
import requests
#import AuthorizationOauth2 #TYMCZASOWE - zeby sie odpalało przy właczeniu 'python webhook.py'
import base64
import time
import configparser
import os
start_time = time.time()
config = configparser.ConfigParser()
config.read("Oauth2/identity.ini")
htmldir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'strona'))
static = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'strona/styles'))


class flaskAppWebhook():
    app = Flask(__name__,template_folder=htmldir, static_folder=static)
    
    def refresh(self,service_name):

        config.read('identity.ini')
        c = config[service_name.upper()]
        refresh_token = c['refresh_token']
        client_id = c['client_id']
        client_secret = c['client_secret']
        print(f"WEBHOOK >> Odświeżanie tokenu dla >> {client_id}")
        if service_name.lower() == "twitch":
            uri = 'https://id.twitch.tv/oauth2/token'
            dane = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
                }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        elif service_name.lower() == "spotify":
            uri = 'https://accounts.spotify.com/api/token'
            tokenString = f'{client_id}:{client_secret}'
            encoded_client = base64.b64encode(tokenString.encode("utf-8")).decode("utf-8") 

            headers = {"Authorization": f'Basic {encoded_client}'}
            dane = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
            }
        try:
            response = requests.post(uri,headers = headers,data = dane)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            
            if service_name.lower() == "spotify": print(f"string for encoded: {tokenString}, encoded string: {encoded_client}")
            elif service_name.lower() != "spotify":
                print(f"Coś poszło nie tak, kod {e}")
                print(headers)
                print(dane)
                print(uri)
        json = response.json()
        if json.get('access_token'):   
            print("WEBHOOK >> ACCESS TOKEN")
            expires_in = json.get('expires_in')
            expires_seconds = time.time() + expires_in
            expires_at = time.localtime(expires_seconds)
            expires_at = time.strftime("%m-%d %H:%M:%S",expires_at)
            print ("WEBHOOK >> Wygenerowano, nowy token wygaśnie w dniu >> ",expires_at)
            config.set(service_name.upper(),'access_token',json.get('access_token'))
            config.set(service_name.upper(),'expires_in',str(expires_seconds))
            config.set(service_name.upper(),'data_waznosci',expires_at)
            if service_name.lower() != 'spotify': config.set(service_name.upper(),'refresh_token',json.get('refresh_token'))
            with open ('Oauth2/identity.ini', 'w') as plik:
                config.write(plik)
        
        return json


    def background_token_refresh(self):
        while True:

            config.read("Oauth2/identity.ini")
            csp = float(config['SPOTIFY']['expires_in'])
            ctw = float(config['TWITCH']['expires_in'])
            aktualny_czas = time.time()
            if csp < aktualny_czas:
                self.refresh("SPOTIFY")
            elif ctw < aktualny_czas:
                self.refresh("TWITCH")
            else:
                pass
            time.sleep(1)


    def send(code, service_name,client_id,client_secret,redirect_uri):
        if service_name.lower() == "twitch":
            dane = {
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'grant_type': "authorization_code",
                'redirect_uri': redirect_uri,
            }
            uri = 'https://id.twitch.tv/oauth2/token?'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            base64_string = None #bo spotify takie ma
        elif service_name.lower() == "spotify":
            client_encoded = client_id + ":" + client_secret
            sample_string_bytes = client_encoded.encode("ascii")    
            base64_bytes = base64.b64encode(sample_string_bytes)
            base64_string = base64_bytes.decode("ascii")
            dane = {
                'code': code,
                'grant_type': "authorization_code",
                'redirect_uri': redirect_uri
                }
            uri = "https://accounts.spotify.com/api/token"
            headers = {
                "Authorization": "Basic " + base64_string
                }
        #wyślij POST z kodem, zwraca access token
        odp = requests.post(uri,headers = headers , data = dane)
        json = odp.json()

        print(f"WEBHOOK >> Autoryzacja {service_name} >> response {odp.status_code}")
        
        return json
    






    @app.route('/', methods=['GET'])
    
    def index():
        return render_template('index.html')
    

    @app.route('/callback', methods=['GET'])
    def handle_callback():
            code = request.args.get('code') #pobiera ten jebany kod
            scope = request.args.getlist('scope') #pobiera scope permisji //lista
            state = request.args.get('state')
            #znajdz czy to request ze spotify czy twitch
            if state:
                service_name = "TWITCH"
                c = config[service_name]
                json = flaskAppWebhook.send(code,c['service_name'],c['client_id'],c['client_secret'],c['redirect_uri'])#json z tokenem, z odpowiedzi po wyslaniu kodu
                access_token = json.get('access_token')
                refresh_token = json.get('refresh_token')
                config.set(service_name,'access_token', access_token)
                config.set(service_name,'refresh_token', refresh_token)

                print("============================================\n")
                print(scope)
                print("============================================\n")
                with open('Oauth2/identity.ini','w') as f:
                     config.write(f)
            else:
                service_name = "SPOTIFY"
                c = config[service_name] #nie jestem z tego dumny, ale działa (mozna sprawdzic czy to twitch czy spotify po zwroconym scope, czy zgadza sie z identity.ini, ale to trzeba przerabiać z urlencoded a mi sie nie chce)
                json = flaskAppWebhook.send(code,c['service_name'],c['client_id'],c['client_secret'],c['redirect_uri'])#json z tokenem, z odpowiedzi po wyslaniu kodu
                access_token = json.get('access_token')
                refresh_token = json.get('refresh_token')
                config.set(service_name,'access_token', access_token)
                config.set(service_name,'refresh_token', refresh_token)
                with open('Oauth2/identity.ini','w') as f:
                    config.write(f)
            if access_token:
                return render_template("authorized.html",token=access_token,refresh = refresh_token)
            else:
                return render_template("notauthorized.html")

   

