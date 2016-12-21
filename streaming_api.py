import tweepy
import json
import datetime
import multiprocessing
import time
from models import Retweet, Reply, Hashtag, TrumpStatus, db

#https://dev.twitter.com/streaming/overview/request-parameters
#specify these parameters as key word arguments to Tweepy

class TrumpTwitterAnalyzer:
    def retweets_of_trump_data(self, json_data):
        """Logs all retweets of Trump's statuses.

        """
        try:
            hashtags = json_data['entities']['hashtags']
            retweeted_status = json_data['retweeted_status']
            rt = Retweet.create(
                    status_id_of_retweeted_tweet=retweeted_status['id_str'],
                    user_id=json_data['user']['id_str'], # do not even need, just here for possible testing
                    location=json_data['user']['location'],
                    created_at=datetime.datetime.fromtimestamp(float(json_data['timestamp_ms'])/1000.0),
                )
            self._store_hashtags(rt, hashtags)

            return {
                    'activity_type': 'retweet',
                    'hashtags': hashtags if hashtags else None,
                    'status_id_of_retweeted_tweet': retweeted_status['id_str'],
                    'user_id': json_data['user']['id_str'], # do not even need, just here for possible testing
                    'location': json_data['user']['location'],
                    'created_at': datetime.datetime.fromtimestamp(float(json_data['timestamp_ms'])/1000.0),
                }
        except Exception as e:
            print(e)

    def replies_to_trump_statuses(self, json_data):
        """Logs all replies to Trump's statuses.

        """
        try:
            hashtags = json_data['entities']['hashtags']

            r = Reply.create(
                    in_reply_to_status_id_str=json_data['in_reply_to_status_id_str'],
                    user_id=json_data['user']['id_str'], # do not even need, just here for possible testing
                    location=json_data['user']['location'],
                    created_at=datetime.datetime.fromtimestamp(float(json_data['timestamp_ms'])/1000.0),
                )
            self._store_hashtags(r, hashtags)

            return {
               'activity_type': 'reply',
               'in_reply_to_status_id_str': json_data['in_reply_to_status_id_str'],
               'hashtags': hashtags if hashtags else None,
               'user_id': json_data['user']['id_str'], # do not even need, just here for possible testing
               'location': json_data['user']['location'],
               'created_at': datetime.datetime.fromtimestamp(float(json_data['timestamp_ms'])/1000.0),
            }
        except Exception as e:
            print(e)

    def trump_statuses(self, json_data):
        """Logs all trump statuses.

        """
        try:
            hashtags = json_data['entities']['hashtags']
            is_retweet = json_data.get('retweeted_status', False)
            if not is_retweet:
                s = TrumpStatus.create(
                        status_id=json_data['id_str'],
                        created_at=datetime.datetime.fromtimestamp(float(json_data['timestamp_ms'])/1000.0),
                        text=json_data['text']
                    )
                self._store_hashtags(s, hashtags)

                return {
                   'activity_type': 'status',
                   'status_id': json_data['id_str'],
                   'hashtags': hashtags if hashtags else None,
                   'created_at': datetime.datetime.fromtimestamp(float(json_data['timestamp_ms'])/1000.0),
                   'text': json_data['text']
                }
        except Exception as e:
            print(e)

    def query(self):
        pass
        # Example query with the reverse foreign key
        # import models
        # m = models.Retweet.select().join(models.Hashtag).where(models.Hashtag.hashtag=="BackstabberHannity")

    def _store_hashtags(self, model_instance, hashtags):

        for hashtag in hashtags:
            h = Hashtag()
            if model_instance.__class__.__name__ == "Reply":
                h.reply = model_instance
            elif model_instance.__class__.__name__ == "TrumpStatus":
                h.trump_status = model_instance
            else:
                h.retweet = model_instance

            h.hashtag = hashtag['text']
            h.save()


class TwitterStreamListener(tweepy.StreamListener):

    def __init__(self, trump_twitter_analyzer, *args, **kwargs):
        self.trump_twitter_analyzer = trump_twitter_analyzer
        self.json_data_list = []
        super().__init__(*args, **kwargs)

    def store_json_data(self, json_data_list):
        # start = time.clock()
        try:
            db.connect()
            trump_twitter_id = "25073877"
            for json_data in json_data_list:
                is_trump_activity = json_data['user']['id_str'] == trump_twitter_id
                if is_trump_activity:
                    self.trump_twitter_analyzer.trump_statuses(json_data)
                else:
                    is_retweet = json_data.get('retweeted_status', False)
                    if is_retweet:
                        self.trump_twitter_analyzer.retweets_of_trump_data(json_data)
                    else:
                        self.trump_twitter_analyzer.replies_to_trump_statuses(json_data)
        except Exception as e:
            print(e)
        finally:
            db.close()

        # end = time.clock()
        # print("Time: ", end - start)


    def on_data(self, data):
        json_data = json.loads(data)
        self.json_data_list.append(json_data)
        if len(self.json_data_list) > 500:
            p = multiprocessing.Process(target=self.store_json_data, args=(self.json_data_list[:],))
            self.json_data_list = []
            p.start()

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))

if __name__ == '__main__':
    from keys import *

    try:
        Reply.create_table()
        Retweet.create_table()
        Hashtag.create_table()
        TrumpStatus.create_table()
        print("New tables made")
    except:
        print("Table/s already exist")

    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    tweepy_api = tweepy.API(auth)

    TwitterStreamListener = TwitterStreamListener(TrumpTwitterAnalyzer())
    twitterStream = tweepy.Stream(auth=tweepy_api.auth, listener=TwitterStreamListener)
    trump_twitter_id = "25073877"
    networks_group_id = "804836955485859841" # for testing on our account @networks_group
    twitterStream.filter(follow=[trump_twitter_id], stall_warnings=True)