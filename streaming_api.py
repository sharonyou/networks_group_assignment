import tweepy
import json
from models import Retweet, Reply, Mention, Hashtag

#https://dev.twitter.com/streaming/overview/request-parameters
#specify these parameters as key word arguments to Tweepy

class TrumpTwitterAnalyzer:
    def retweets_of_trump_data(self, json_data):
        """Logs all retweets of Trump's statuses.

        """
        hashtags =  json_data['entities']['hashtags']
        retweeted_status = json_data['retweeted_status']
        self._store_hashtags(json_data)

        Retweet(
                activity_type='retweet',
                status_id_of_retweeted_tweet=retweeted_status['id_str'],
                user_id=json_data['user']['id_str'], # do not even need, just here for possible testing
                location=json_data['user']['location'],
                timestamp_ms=json_data['timestamp_ms'],
            ).save()
        return {
                'activity_type': 'retweet',
                'hashtags': hashtags if hashtags else None,
                'status_id_of_retweeted_tweet': retweeted_status['id_str'],
                'user_id': json_data['user']['id_str'], # do not even need, just here for possible testing
                'location': json_data['user']['location'],
                'timestamp_ms': json_data['timestamp_ms'],
            }

    def replies_to_trump_statuses(self, json_data):
        """Logs all replies to Trump's statuses.

        """
        hashtags = json_data['entities']['hashtags']
        self._store_hashtags(json_data)

        Reply(
                activity_type='reply',
                in_reply_to_status_id_str=json_data['in_reply_to_status_id_str'],
                user_id=json_data['user']['id_str'], # do not even need, just here for possible testing
                location=json_data['user']['location'],
                timestamp_ms=json_data['timestamp_ms']
        ).save()
        return {
           'activity_type': 'reply',
           'in_reply_to_status_id_str': json_data['in_reply_to_status_id_str'],
           'hashtags': hashtags if hashtags else None,
           'user_id': json_data['user']['id_str'], # do not even need, just here for possible testing
           'location': json_data['user']['location'],
           'timestamp_ms': json_data['timestamp_ms'],
        }

    def mentions_of_trump(self, json_data):
        """Logs all mentions of Trump that are not replies to his statuses.

        """
        hashtags = json_data['entities']['hashtags']
        self._store_hashtags(json_data)
        
        Mention(
                activity_type='mention',
                user_id=json_data['user']['id_str'], # do not even need, just here for possible testing
                location=json_data['user']['location'],
                timestamp_ms=json_data['timestamp_ms'],
        ).save()
        return {
                'activity_type': 'mention',
                'hashtags': hashtags if hashtags else None,
                'user_id': json_data['user']['id_str'], # do not even need, just here for possible testing
                'location': json_data['user']['location'],
                'timestamp_ms': json_data['timestamp_ms'],
        }

    def _store_hashtags(self, json_data):
        pass

class TwitterStreamListener(tweepy.StreamListener):

    def __init__(self, trump_twitter_analyzer, *args, **kwargs):
        self.trump_twitter_analyzer = trump_twitter_analyzer
        super().__init__(*args, **kwargs)

    

    def on_data(self, data):
        json_data = json.loads(data)

        trump_twitter_id = "25073877"
        in_reply_to_status_id_str = json_data['in_reply_to_status_id_str']
        in_reply_to_user_id_str = json_data['in_reply_to_user_id_str']
        is_reply = in_reply_to_user_id_str == trump_twitter_id and in_reply_to_status_id_str

        is_retweet = json_data.get('retweeted_status', False)

        is_mention = False
        for user in json_data['entities']['user_mentions']:
            if user['id_str'] == trump_twitter_id:
                is_mention = True
                break

        retweet = reply = mention = None
        if is_retweet:
            retweet = self.trump_twitter_analyzer.retweets_of_trump_data(json_data)
            print(retweet)
        elif is_reply:
            reply = self.trump_twitter_analyzer.replies_to_trump_statuses(json_data)
            print(reply)
        #is_mention must be last to avoid catching all the replies
        elif is_mention:
            mention = self.trump_twitter_analyzer.mentions_of_trump(json_data)
            print(mention)

if __name__ == '__main__':
    consumer_key = "zaQml4DgkhjmCLhJ5KC90jeuM"
    consumer_secret = "kcOhiBG3nL3Hl9IgfdVC62QMYkmt7Fs1kdYqgaeyUqfWudwXrI"
    access_token = "804836955485859841-BGEwCIwrvSCZmW9YE7mbvAl6ni2WOi3"
    access_token_secret = "1V6apviXNqtYyS2hIc4FqIgtep09AMvbDBIsEXfG9ZQal"

    try:
        Reply.create_table()
        Mention.create_table()
        Retweet.create_table()
        Hashtag.create_table()
        print("New tables made")
    except:
        print("Table/s already exist")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    tweepy_api = tweepy.API(auth)

    TwitterStreamListener = TwitterStreamListener(TrumpTwitterAnalyzer())
    twitterStream = tweepy.Stream(auth=tweepy_api.auth, listener=TwitterStreamListener)
    trump_twitter_id = "25073877"
    networks_group_id = "804836955485859841" # for testing on our account @networks_group
    twitterStream.filter(follow=[trump_twitter_id], stall_warnings=True)
