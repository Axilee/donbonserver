import webbrowser
import configparser
config = configparser.ConfigParser()
config.read("Oauth2/identity.ini")

def getOAuth(service_name,client_id,link,redirect_uri):
    c = config[service_name.upper()]
    if(service_name.lower() == "twitch"):
        print("oauth2 twitch")
        client_uri = f"authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope="
        l = c["scope"] 
        l = l.replace(":","%3A")
        scope = l.replace(",","+")
    elif(service_name.lower() == "spotify"):
        print("oauth2 spotify")
        client_uri = f"authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope="
        l = c["scope"] 
        l = l.replace(":","%3A")
        scope = l.replace(",","+")
    else:
        return "sraka"
                    
    if(service_name == "spotify"):
        link = link+client_uri+scope
    elif(service_name == "twitch"):
        link = link+client_uri+scope+"&state=c3ab8aa609ea11e793ae92361f002671"
        print(link)
    
    webbrowser.open(link)
if __name__ == "__main__":
    getOAuth()
#https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=nohxc0resfams2ui1ftvvs07awax2c&redirect_uri=http://localhost&scope=channel%3Amanage%3Apolls+channel%3Aread%3Apolls+bits%3Aread&state=c3ab8aa609ea11e793ae92361f002671

