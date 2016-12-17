from peewee import *

db = SqliteDatabase("trump.db")

class Retweet(Model):
    status_id_of_retweeted_tweet = CharField()
    user_id = CharField()
    location = CharField(null=True)
    timestamp_ms = CharField()

    class Meta:
        database = db

class Reply(Model):
    in_reply_to_status_id_str = CharField(null=True)
    user_id = CharField()
    location = CharField(null=True)
    timestamp_ms = CharField()
    
    class Meta:
        database = db

class Hashtag(Model):
    retweet = ForeignKeyField(Retweet, null=True, related_name="hashtags")
    reply = ForeignKeyField(Reply, null=True, related_name="hashtags")
    hashtag = CharField()

    class Meta:
        database = db


def populate_test_data():

    for i in range(5):
        r = Reply(
              in_reply_to_status_id_str="reply status_id: " + str(i),
              user_id = "user_id: " + str(i),
              location = "location: " + str(i),
              timestamp_ms = "time: " + str(i))


        rt = Retweet(
                 status_id_of_retweeted_tweet = "status_id " + str(i),
                 user_id = "user_id: " + str(i),
                 location = "location: " + str(i),
                 timestamp_ms = "timestamp_ms: " + str(i))

        r.save()
        rt.save()
        Hashtag(reply=r, hashtag="#michael #is #awesome" + str(i)).save()
        Hashtag(rt=rt, hashtag="#michael #is #awesome" + str(i)).save()

if __name__ == '__main__':
    try:
        print("creating new tables. Adding data.")
        Reply.create_table()
        Retweet.create_table()
        Hashtag.create_table()
        try:
            populate_test_data()
        except Exception as e:
            print(e)

    except OperationalError:
        print("table/s already exist. Adding data.")
        try:
            populate_test_data()
        except Exception as e:
            print(e)
