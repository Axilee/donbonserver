
from dotenv import load_dotenv
import os
import openai
load_dotenv()
print(os.getenv("key"))
openai.api_key = os.getenv("key")

def obraz(prompt):
   
    msg = [
        {"role": "system", "content": "You are roleplaying as a really offensive twitch viewer called DonBon, and you're watching a guy called DonHoman. His name is Kuba Homanowski also called homan. You only respond in polish. You are to write a mean message like a shitposter, responding to the message sent by user. Write like you're writing a typical twitch chat message. You have to use very explicit casual polish language, using polish, modern slang. Refer to polish memes. Make sure your answer is written in native polish. Avoid using words that go against twitch's terms of service. Write up to 2 sentences. Do not use the word 'gracz'. Use standard twitch emotes in your response.  Do you understand?"},
        {"role": "assistant", "content":"Tak."},
        {"role": "user","content":prompt}
    ]
    odp = chatgpt(msg)
    print (odp)
    return odp
   
    

def tytul(prompt):
    msg = [
        {"role": "system", "content": "You are an assistant that creates funny and creative titles for twitch streams You are to create a title for a streamer. The user will list the different separate games or events the stream will contain. The title should be written in native polish. It has to be stupid. Use a polish pun, if possible.  Do you understand?"},
        {"role": "assistant", "content":"Tak."},
        {"role": "user","content":prompt}
    ]
    odp = chatgpt(msg)
    print(odp)
    return odp

def chatgpt(msg):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg,
        max_tokens=2500,
        n=1,
        temperature=0.90,
    )
    odpowiedz = response.choices[0].message.content
    return odpowiedz


