import tweepy

# tweepy docs - http://tweepy.readthedocs.io/en/v3.5.0/getting_started.html

consumer_key = "zaQml4DgkhjmCLhJ5KC90jeuM" #api key
consumer_secret = "kcOhiBG3nL3Hl9IgfdVC62QMYkmt7Fs1kdYqgaeyUqfWudwXrI" #api secret
access_token = "804836955485859841-BGEwCIwrvSCZmW9YE7mbvAl6ni2WOi3"
access_token_secret = "1V6apviXNqtYyS2hIc4FqIgtep09AMvbDBIsEXfG9ZQal"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

tweepy_api = tweepy.API(auth)
trump_twitter_id = "25073877"
trump_username = "realDonaldTrump"


# print(tweepy_api.get_user(id=trump_twitter_id))
# print(tweepy_api.user_timeline(id=trump_twitter_id)[0].id)
# print(tweepy_api.get_status(id="804848711599882240"))
# to deal with rate limiting we will have to do sampling
print(tweepy_api.retweets(id="804848711599882240"))
# print(tweepy_api.mentions_timeline(count=1))

# TODO: Get the id's of every user that retweeted something, but need to find a way
# to do it that gets around Twitter's limit of 100 id's of people retweeting

# This may work: http://stackoverflow.com/questions/6316899/how-to-get-a-list-of-all-retweeters-in-twitter

