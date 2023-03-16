import tweepy
import sys
import random as rng

consumer_key = "mDCoAcNnX4ZfFH30poPKiTIzX"
consumer_secret = "fUUKJkN9sExQ5Ic1CrqG978ncSczjJtLzJvLiTiKaUcsvchpPs"
access_token = "1526348621741973508-DXzxCV74lw13a2yydlJxoPKmc4fmKh"
access_token_secret = "37SiWkdyfF40pe5SDpcL9YP1I3y8no9sMqhBeeftOd51Z"


client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)

# Create Tweet
# The app and the corresponding credentials must have the Write permission

# Check the App permissions section of the Settings tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps

# Make sure to reauthorize your app / regenerate your access token and secret
# after setting the Write permission

frases = ["Simulação finalizada","VRAU!","FINALMENTE ACABOU","Hora do descanso dos justos","Talvez tenha dado errado, rs rs","C A V A L O",\
"Pra comemorar https://www.youtube.com/watch?v=dQw4w9WgXcQ","Acabei 🌈👩‍🔬‍✨🎇","👁👄👁","ERRO??"]

t = sys.argv[1]
response = client.create_tweet(
 #text = frases[rng.randint(0,len(frases))] + "\n @ Wanda @farinha96br \n --runtime:" + t
 text = "Hello Julian"

)
print(f"https://twitter.com/user/status/{response.data['id']}")





#
