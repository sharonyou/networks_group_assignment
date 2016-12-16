from peewee import *

db = SqliteDatabase("trump.db")

class Retweet(Model):
    activity_type = CharField()
    status_id_of_retweeted_tweet = CharField()
    user_id = CharField()
    location = CharField(null=True)
    timestamp_ms = CharField()

    class Meta:
        database = db

class Mention(Model):
    activity_type = CharField()
    user_id = CharField()
    location = CharField(null=True)
    timestamp_ms = CharField()

    class Meta:
        database = db

class Reply(Model):
    activity_type = CharField()
    in_reply_to_status_id_str = CharField()
    user_id = CharField()
    location = CharField(null=True)
    timestamp_ms = CharField()
    
    class Meta:
        database = db

class Hashtag(Model):
    retweet = ForeignKeyField(Retweet, null=True, related_name="hashtags")
    reply = ForeignKeyField(Reply, null=True, related_name="hashtags")
    mention = ForeignKeyField(Mention, null=True, related_name="hashtags")
    hashtag = CharField()

    class Meta:
        database = db


def populate_test_data():

    for i in range(5):
        r = Reply(activity_type="Reply",
              status_id_of_retweeted_tweet="status_id: " + str(i),
              in_reply_to_status_id_str="reply status_id: " + str(i),
              user_id = "user_id: " + str(i),
              location = "location: " + str(i),
              timestamp_ms = "time: " + str(i))


        rt = Retweet(activity_type="Retweet",
                 status_id_of_retweeted_tweet = "status_id " + str(i),
                 user_id = "user_id: " + str(i),
                 location = "location: " + str(i),
                 timestamp_ms = "timestamp_ms: " + str(i))

    
        m = Mention(activity_type="Mention",
                user_id="user_id: " + str(i),
                location="location: " + str(i),
                timestamp_ms = "timestamp_ms " + str(i))
        m.save()
        r.save()
        rt.save()

        for j in range(3):
            choices = (r, rt, m)
            if i == 0:
                Hashtag(reply=choices[j].id, hashtag="#michael #is #awesome" + str(j)).save()
            
            elif i == 1:
                Hashtag(rt=choices[j].id, hashtag="#michael #is #awesome" + str(j)).save()

            else:
                Hashtag(m=choices[j].id, hashtag="#michael #is #awesome" + str(j)).save()

if __name__ == '__main__':
    try:
        Reply.create_table()
        Mention.create_table()
        Retweet.create_table()
        Hashtag.create_table()
        try:
            populate_test_data()
        except Exception as e:
            print(e)
            print("initial populate failed")

    except OperationalError:
        print("table/s already exist. Adding data: ")
        try:
            populate_test_data()
        except Exception as e:
            print(e)
            print("populate failed")
