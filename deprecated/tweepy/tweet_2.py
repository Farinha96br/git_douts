import tweepy

consumer_key = "mDCoAcNnX4ZfFH30poPKiTIzX"
consumer_secret = "fUUKJkN9sExQ5Ic1CrqG978ncSczjJtLzJvLiTiKaUcsvchpPs"
access_token = "1526348621741973508-DXzxCV74lw13a2yydlJxoPKmc4fmKh"
access_token_secret = "37SiWkdyfF40pe5SDpcL9YP1I3y8no9sMqhBeeftOd51Z"


auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)

tweet_text='TEXTOOOO'
image_path ="teste.png"

#Generate text tweet with media (image)
status = api.media_upload(image_path)
api.update_status(status=tweet_text)





#
