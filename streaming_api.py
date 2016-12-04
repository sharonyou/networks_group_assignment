import tweepy
import json

#https://dev.twitter.com/streaming/overview/request-parameters
#specify these parameters as key word arguments to Tweepy

consumer_key = "zaQml4DgkhjmCLhJ5KC90jeuM" #api key
consumer_secret = "kcOhiBG3nL3Hl9IgfdVC62QMYkmt7Fs1kdYqgaeyUqfWudwXrI" #api secret
access_token = "804836955485859841-BGEwCIwrvSCZmW9YE7mbvAl6ni2WOi3"
access_token_secret = "1V6apviXNqtYyS2hIc4FqIgtep09AMvbDBIsEXfG9ZQal"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

tweepy_api = tweepy.API(auth)
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
        
    # def on_data(self, data):
    #     print(data)
        
    def on_data(self, data):
        # print("This is the data", data)
        data_dict = json.loads(data)
        print(data_dict.keys())
        print("This is place: ", data_dict['place'])
        print("This is geo: ", data_dict['geo'])
        print("This is coordinates: ", data_dict['coordinates'])
        print("THis is in_reply_to_status_id", data_dict['in_reply_to_status_id'])
        # print("id_str: ", data_dict['id_str'])
        # print("location: ", data_dict['location'])
        
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = tweepy_api.auth, listener=myStreamListener)
# all the possible parameters: https://dev.twitter.com/streaming/overview/request-parameters
trump_twitter_id = "25073877"
myStream.filter(follow=[trump_twitter_id], stall_warnings=True)
# myStream.filter(locations=[-122.75,36.8,-121.75,37.8])
