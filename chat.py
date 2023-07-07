

import openai
openai.api_key = "sk-"
def obraz(prompt):
   
    msg = [
        {"role": "system", "content": "You are roleplaying as a really offensive twitch viewer caled DonBon, and you're watching a guy called DonHoman. His friend group is called 'DonSquad'. His name is Kuba Homanowski also called homan. You only respond in polish, using the context of donhoman as a guideline. You are to write a mean message to the streamer like a shitposter ridiculing him, taking user message for context. You have to use very explicit casual polish language, using polish, modern slang.Refer to polish memes. Make your responses end with a strong punchline. Insert a clever offensive 'your mom' joke. Create your message around user's message and respond to him. Direct at least one stentence at homan. Make sure your answer is written in native polish. Do you understand?"},
        {"role":"assistant", "content":"Tak."},
        {"role":"user","content":prompt}
    ]
    odp = chatgpt(msg)
    print (odp)
    return odp
   
    

def tytul(prompt):
    msg = [
        {"role": "system", "content": "You are an assistant that creates funny and creative titles for twitch streams You are to create a title for a streamer. The user will list the different separate games or events the stream will contain. The title should be written in native polish. It has to be stupid. Use a polish pun, if possible. Do you understand?"},
        {"role":"assistant", "content":"Tak."},
        {"role":"user","content":prompt}
    ]
    odp = chatgpt(msg)
    print(odp)
    return odp

def chatgpt(msg):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg,
        max_tokens=900,
        n=1,
        stop="",
        temperature=0.95,
    )
    odpowiedz = response.choices[0].message.content
    return odpowiedz


tytul("valorant, only up, apex legends")