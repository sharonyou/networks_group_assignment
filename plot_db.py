import sqlite3
import random
import matplotlib.pyplot as plt
import csv
import math
import sys
import copy
from datetime import datetime, timedelta
import time
from scipy.stats import norm
from models import Retweet, Reply, TrumpStatus, Hashtag
import numpy as np
from random import shuffle
import re
import tweepy

from stalk import verified

def read_tweets():
	for tweet in TrumpStatus.select():
		print('-----------------------------')
		print(tweet.text)
		print('-----------------------------')

def read_times():
	times = []
	for reply in Reply.select():
		time = reply.created_at
		if time:
			times.append(time)
		print(str(reply.created_at) + " , " + str(reply.location))
	return times
    

## PART 1: POPULATION ANALYSIS ('INFECTION')

## given a tweet, time-bucket all retweets and replies until 'timeframe' seconds
def get_responses(trump_status_id,timeframe, interval):
	xData = []  #retweet times
	yData = []  #retweet info
	xData2 = []     #reply times
	yData2 = []     #reply info
	totals = []
	user_bucket_retweets = []
	user_bucket_replies = []

	count = 0
	total = 0
	x = 0
	first = 1
	secondsSince = 0
	users=[]
	user_total = 0
	steps = 0
	locations = []

	for tweet in TrumpStatus.select().where(TrumpStatus.status_id==trump_status_id):
		startTime = datetime.strptime(str(tweet.created_at)[:19],"%Y-%m-%d %H:%M:%S")

	for retweet in Retweet.select().where(Retweet.status_id_of_retweeted_tweet == trump_status_id).order_by(Retweet.created_at):
		s = str(retweet.created_at)[:19]
		t = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

		if first == 1:
			currentTime = startTime
			first = 0

		if (currentTime - startTime) >= timedelta(seconds=timeframe):
			break;

		while t >= currentTime and currentTime not in xData:
			xData.append(currentTime)
			yData.append(count)

			currentTime = currentTime+timedelta(seconds=interval)

			#users_unique = set(users)
			user_bucket_retweets.append(users)
			users = []

		count = count + 1
		total = total + 1
		users.append(retweet.user_id)

	#timebreak = timedelta(seconds = t - startTime)
	#print(len(user_bucket_retweets))
	#print(xData[:10])
	#print(xData[-10:])

	count = 0
	total = 0
	x = 0
	first = 1
	secondsSince = 0
	users=[]
	user_total = 0
	locations=[]

	for reply in Reply.select().where(Reply.in_reply_to_status_id_str == trump_status_id).order_by(Reply.created_at):
		s = str(reply.created_at)[:19]
		t = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

		if first == 1:
			currentTime = startTime
			first = 0

		if (currentTime - startTime) >= timedelta(seconds=timeframe):
			break;

		while t >= currentTime and currentTime not in xData2:
			xData2.append(currentTime)
			yData2.append(count)

			currentTime = currentTime+timedelta(seconds=interval)

			#users_unique = set(users)
			user_bucket_replies.append(users)
			users = []

		count = count + 1
		total = total + 1
		users.append(reply.user_id)


	#print(len(user_bucket_replies))
	#print(xData2[:10])
	#print(xData2[-10:])

	minframe = min(len(xData),len(xData2))
	xData = xData[0:minframe]
	xData2 = xData2[0:minframe]
	yData = yData[0:minframe]
	yData2 = yData2[0:minframe]
	user_bucket_retweets = user_bucket_retweets[0:minframe]
	user_bucket_replies = user_bucket_replies[0:minframe]
	return xData, yData, xData2, yData2, user_bucket_retweets, user_bucket_replies


## same as above with specified location
def get_responses_loc(trump_status_id,timeframe, interval):
	xData = [] #NK
	yData = []
	xData2 = [] #NYE
	yData2 = []
	totals = []
	user_bucket_retweets = []
	user_bucket_replies = []

	count = 0
	total = 0
	x = 0
	first = 1
	secondsSince = 0
	users=[]
	user_total = 0
	steps = 0
	locations = []

	for tweet in TrumpStatus.select().where(TrumpStatus.status_id==trump_status_id):
		startTime = datetime.strptime(str(tweet.created_at)[:19],"%Y-%m-%d %H:%M:%S")

	for retweet in Retweet.select().where(Retweet.status_id_of_retweeted_tweet == trump_status_id).order_by(Retweet.created_at):
		s = str(retweet.created_at)[:19]

		bs = '2000-01-01 5:00:00'
		t = datetime.strptime(bs, "%Y-%m-%d %H:%M:%S")

		if retweet.location:
			if ("England" in retweet.location and "New England" not in retweet.location) or\
			"UK" in retweet.location or "United Kingdom" in retweet.location or "London" in retweet.location or \
			"Birmingham" in retweet.location or "Leeds" in retweet.location or "Glasgow" in retweet.location or\
			"Sheffield" in retweet.location or "Bradford" in retweet.location or\
			"Edinburgh" in retweet.location or "Liverpool" in retweet.location or\
			"Manchester" in retweet.location or "Bristol" in retweet.location:
			#if "Canada" in retweet.location or "Ontario" in retweet.location or "British Columbia" in retweet.location or "Quebec" in retweet.location or "Alberta" in retweet.location or "Saskatchewan" in retweet.location or "Manitoba" in retweet.location:
				t = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
				#print(retweet.location)


		if first == 1:
			currentTime = startTime
			first = 0

		if (currentTime - startTime) >= timedelta(seconds=timeframe):
			break;

		while t >= currentTime and currentTime not in xData:
			xData.append(currentTime)
			yData.append(count)

			currentTime = currentTime+timedelta(seconds=interval)

			#users_unique = set(users)
			user_bucket_retweets.append(users)
			users = []

		if retweet.location:
			if ("England" in retweet.location and "New England" not in retweet.location) or\
			"UK" in retweet.location or "United Kingdom" in retweet.location or "London" in retweet.location or \
			"Birmingham" in retweet.location or "Leeds" in retweet.location or "Glasgow" in retweet.location or\
			"Sheffield" in retweet.location or "Bradford" in retweet.location or\
			"Edinburgh" in retweet.location or "Liverpool" in retweet.location or\
			"Manchester" in retweet.location or "Bristol" in retweet.location:
			#if "Canada" in retweet.location or "Ontario" in retweet.location or "British Columbia" in retweet.location or "Quebec" in retweet.location or "Alberta" in retweet.location or "Saskatchewan" in retweet.location or "Manitoba" in retweet.location:
				count = count + 1
				total = total + 1

				users.append(retweet.user_id)

	#timebreak = timedelta(seconds = t - startTime)
	#print(len(user_bucket_retweets))
	#print(xData[:10])
	#print(xData[-10:])

	count = 0
	total = 0
	x = 0
	first = 1
	secondsSince = 0
	users=[]
	user_total = 0
	locations=[]

	for reply in Reply.select().where(Reply.in_reply_to_status_id_str == trump_status_id).order_by(Reply.created_at):
		s = str(reply.created_at)[:19]

		bs = '2000-01-01 5:00:00'
		t = datetime.strptime(bs, "%Y-%m-%d %H:%M:%S")

		if reply.location:
			if ("England" in reply.location and "New England" not in reply.location) or\
			"UK" in reply.location or "United Kingdom" in reply.location or "London" in reply.location or \
			"Birmingham" in reply.location or "Leeds" in reply.location or "Glasgow" in reply.location or\
			"Sheffield" in reply.location or "Bradford" in reply.location or\
			"Edinburgh" in reply.location or "Liverpool" in reply.location or\
			"Manchester" in reply.location or "Bristol" in reply.location:
			#if "Canada" in reply.location or "Ontario" in reply.location or "British Columbia" in reply.location or "Quebec" in reply.location or "Alberta" in reply.location or "Saskatchewan" in reply.location or "Manitoba" in reply.location:
				t = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

		if first == 1:
			currentTime = startTime
			first = 0

		if (currentTime - startTime) >= timedelta(seconds=timeframe):
			break;

		while t >= currentTime and currentTime not in xData2:
			xData2.append(currentTime)
			yData2.append(count)

			currentTime = currentTime+timedelta(seconds=interval)

			#users_unique = set(users)
			user_bucket_replies.append(users)
			users = []

		if reply.location:
			if ("England" in reply.location and "New England" not in reply.location) or\
			"UK" in reply.location or "United Kingdom" in reply.location or "London" in reply.location or \
			"Birmingham" in reply.location or "Leeds" in reply.location or "Glasgow" in reply.location or\
			"Sheffield" in reply.location or "Bradford" in reply.location or\
			"Edinburgh" in reply.location or "Liverpool" in reply.location or\
			"Manchester" in reply.location or "Bristol" in reply.location:
			#if "Canada" in reply.location or "Ontario" in reply.location or "British Columbia" in reply.location or "Quebec" in reply.location or "Alberta" in reply.location or "Saskatchewan" in reply.location or "Manitoba" in reply.location:
				count = count + 1
				total = total + 1

				users.append(reply.user_id)


	#print(len(user_bucket_replies))
	#print(xData2[:10])
	#print(xData2[-10:])

	minframe = min(len(xData),len(xData2))
	xData = xData[0:minframe]
	xData2 = xData2[0:minframe]
	yData = yData[0:minframe]
	yData2 = yData2[0:minframe]
	user_bucket_retweets = user_bucket_retweets[0:minframe]
	user_bucket_replies = user_bucket_replies[0:minframe]
	return xData, yData, xData2, yData2, user_bucket_retweets, user_bucket_replies

## align response/retweet data to facilitate analysis of total responses
def get_sums_2(xData, yData, xData2, yData2, user_bucket_retweets, user_bucket_replies):
	user_bucket_all = []
	user_counts_all = []
	user_count = 0
	for t in range(0,len(xData)):
		user_bucket_temp = []
		if user_bucket_retweets[t]:
			user_bucket_temp.extend(user_bucket_retweets[t])
		if user_bucket_replies[t]:
			user_bucket_temp.extend(user_bucket_replies[t])
		user_bucket_all.append(list(set(user_bucket_temp)))
		user_count = user_count+len(user_bucket_all[t])
		user_counts_all.append(user_count)

	return xData, [sum(i) for i in zip(yData,yData2)], user_counts_all, user_bucket_all


# MAGA
#xData, yData, xData2, yData2, user_bucket_retweets, user_bucket_replies= get_responses(815930688889352192,80000,3600)#815185071317676033, 80000, 10)

# NYE
# xData, yData, xData2, yData2, user_bucket_retweets, user_bucket_replies= get_responses(815185071317676033,80000,10)#815185071317676033, 80000, 10)

# ISRAEL
#xData, yData, xData2, yData2, user_bucket_retweets, user_bucket_replies= get_responses(811928543366148096,80000,10)#815185071317676033, 80000, 10)

# NK
xData, yData, xData2, yData2, user_bucket_retweets, user_bucket_replies= get_responses(816057920223846400,80000,1800)#815185071317676033, 80000, 10)

# RUSSIA
#xData, yData, xData2, yData2, user_bucket_retweets, user_bucket_replies= get_responses(814958820980039681,80000,3600)#815185071317676033, 80000, 10)

times, sum_data, sum_users, user_bucket_all = get_sums_2(xData, yData, xData2, yData2, user_bucket_retweets, user_bucket_replies)


'''
## plot retweets and replies
fig = plt.figure()
fig.suptitle("Retweets over Times", fontsize=20)
plt.xlabel("Seconds after Tweet", fontsize=18)
#plt.ylabel("Retweets", fontsize=18)

plt.plot(xData, yData, lw = 1, label = 'Retweets')
plt.plot(xData2, yData2, lw = 1, label = 'Replies')

## plot all responses
plt.plot(times, sum_data, lw = 1, label = 'Total Responses')

## plot all unique users
#plt.plot(times, sum_users, lw = 1, label = 'Users')

plt.legend( loc='upper left' )


# 90% marks
yData = np.array(yData)
idx = np.argwhere(np.diff(np.sign(yData - yData[-1]*0.9)) != 0).reshape(-1) + 0
plt.plot(xData[idx[0]], yData[idx[0]], 'ro')

yData2 = np.array(yData2)
idx2 = np.argwhere(np.diff(np.sign(yData2 - yData2[-1]*0.9)) != 0).reshape(-1) + 0
plt.plot(xData2[idx2[0]], yData2[idx2[0]], 'ro')

#sum_data = np.array(sum_data)
#idx3 = np.argwhere(np.diff(np.sign(sum_data - totals[2]*0.9)) != 0).reshape(-1) + 0
#plt.plot(times[idx3[0]], sum_data[idx3[0]], 'ro')

#print(xData[idx[0]], xData2[idx2[0]], times[idx3[0]])

plt.show()

'''

## align response info over two tweets to enable plotting together
def two_tweets(s1,s2,tf,iv):
	a1,b1,c1,d1,e1,f1= get_responses(s1,tf,iv)
	a2,b2,c2,d2,e2,f2= get_responses(s2,tf,iv)
	x1,y1,z1,w1=get_sums_2(a1,b1,c1,d1,e1,f1)
	x2,y2,z2,w2=get_sums_2(a2,b2,c2,d2,e2,f2)

	x,y,z,w = get_sums_2(x1, y1, x2, y2, w1, w2)

	return x1,y1,x2,y2,x,y,z,w


'''
x1,y1,x2,y2,x,y,z,w=two_tweets(816057920223846400,816068355555815424,80000,3600)
print(len(x1))
print(len(x2))
print(len(x))

## plot retweets and replies
fig = plt.figure()
fig.suptitle("Retweets over Times", fontsize=20)
plt.xlabel("Seconds after Tweet", fontsize=18)
#plt.ylabel("Retweets", fontsize=18)
plt.plot(x, y1[:len(x)], lw = 1, label = 'Tweet 1')

# a1 instead of a2 if want align
plt.plot(x, y2[:len(x)], lw = 1, label = 'Tweet 2')

## plot all responses
plt.plot(x, y, lw = 1, label = 'Both')

## plot all responses
plt.plot(x, [i / 2 for i in y], lw = 1, label = 'Average')

## plot all unique users
#plt.plot(x, z, lw = 1, label = 'Users')

plt.legend(loc = 'upper left')

#plt.axhline(y=(totals[0]*0.9), color='r', linestyle='-')
#plt.axhline(y=(totals[1]*0.9), color='r', linestyle='-')


plt.show()
'''

## sampling by population characteristics for 'factoring'
def analyze_users_rand(user_bucket_all):
	f2 = open('nk-verified-hh4-50p.txt', 'a')

	for t in range(4,5):
		count = 0
		print(str(t))
		print(times[t])
		f2.write(str(t)+'\n')
		f2.write(str(times[t])+'\n')
		tmp = user_bucket_all[t]
		shuffle(tmp)
		for user in tmp[:len(user_bucket_all[t])//2]:
			print('user: ')
			search_url = 'https://twitter.com/intent/user?user_id='+user
			if verified(search_url):
				f2.write('user: '+user +'\n')
				count+=1

		f2.write('verified: ' + str(count) +'\n'+'\n')

	f2.close()
    
'''
analyze_users_rand(user_bucket_all)
'''
    
    
    
## PART 2: NEIGHBOR ANALYSIS ('NODE-FLIPPING')

# 'node-flipping' analysis
def analyze_friends_rand(user_bucket_all):
	#consumer_key = "zaQml4DgkhjmCLhJ5KC90jeuM" #api key
	consumer_key = "9XZmW5hg6NgFigaSFQysV6vFJ" #api key
	#consumer_secret = "kcOhiBG3nL3Hl9IgfdVC62QMYkmt7Fs1kdYqgaeyUqfWudwXrI" #api secret
	consumer_secret = "yRNf4dHWELgzGsgc9Im720FTvQAXMLNa7tHi1ChtP5rYx7Y9xN"
	#access_token = "804836955485859841-BGEwCIwrvSCZmW9YE7mbvAl6ni2WOi3"
	access_token = "1360622402-m4Jw2jffjYTu2EmNnHcp822cu5nI1ZvK9nonp97"
	#access_token_secret = "1V6apviXNqtYyS2hIc4FqIgtep09AMvbDBIsEXfG9ZQal"
	access_token_secret = "x96tlafZMkHhF35iRuNELNJkf1yReqr5e37sCc6e42631"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

	probs = []

	for t in range(1,13):
		print(str(t))
		print(times[t])
		total = 0
		tmp = user_bucket_all[t]
		shuffle(tmp)
		for user in tmp[:10]:
			count_any = 0
			count = 0
			print('user: '+user)
			user_account = api.get_user(user)
			print('friends:')
			for friend in user_account.friends(count=200):
				#if str(friend.id) in user_bucket_all[:t]:
				present = 0
				for i in range(0,t):
					if str(friend.id) in user_bucket_all[i]:
						present = 1

				if present == 1:
					count = count+1
					print(str(friend.id) + '***')
				else:
					print(str(friend.id))

				count_any = count_any+1
			print('count: '+ str(count) +'\n')
			print('of: '+ str(count_any) +'\n')

		probs.append(total/200*10)

	return probs

#print(len(user_bucket_all[0]))
#print(len(user_bucket_all[1]))
#print(len(user_bucket_all[2]))
#print(len(user_bucket_all[3]))

'''
p = analyze_friends_rand(user_bucket_all)
plt.plot(times[:12], p, lw = 1, label = '# Neighbors')
'''

# set up plots for 'node-flipping' analysis after running analyze_friends_rand()
def graph_probs(file,hours):
	hours = int(hours)
	with open(file, "r") as ins:
		counts = []
		samples = []
		for line in ins:
			if 'count' in line:
				counts.append(int(re.sub(':','',line[-3:-1])))
			if 'of' in line:
				tmp = int(re.sub(':','',line[-4:-1]))
				if tmp == 0:
					tmp = 1000000
				samples.append(tmp)

	print(counts)
	print(samples)

	sample_probs = [a/b for a,b in zip(counts,samples)]
	sample_prob_avgs_nonzero = []
	sample_count_avgs_nonzero = []
	sample_prob_avgs = []
	sample_count_avgs = []
	prob_maxs = []
	count_maxs = []
	prob_min_nonzero = []
	count_min_nonzero = []
	nonzeros = []
	for i in range(0,hours):
		nz = 0
		take_mean_prob = []
		take_mean_count = []
		nz_min_prob = 100
		nz_min_count = 100
		for j in range(0,10):
			#if samples[i*10+j]== 0:
			#	continue

			if counts[i*10+j] != 0:
				take_mean_prob.append(sample_probs[i*10+j])
				take_mean_count.append(counts[i*10+j])
				nz = nz+1
				if sample_probs[i*10+j] < nz_min_prob:
					nz_min_prob = sample_probs[i*10+j]
				if counts[i*10+j] < nz_min_count:
					nz_min_count = counts[i*10+j]
		if nz_min_prob == 100:
			nz_min_prob = 0
		if nz_min_count == 100:
			nz_min_count = 0
		sample_prob_avgs_nonzero.append(np.mean(take_mean_prob))
		sample_count_avgs_nonzero.append(np.mean(take_mean_count))
		sample_prob_avgs.append(np.mean(sample_probs[i*10:(i+1)*10]))
		sample_count_avgs.append(np.mean(counts[i*10:(i+1)*10]))
		prob_maxs.append(max(sample_probs[i*10:(i+1)*10]))
		count_maxs.append(max(counts[i*10:(i+1)*10]))
		nonzeros.append(nz/10)
		prob_min_nonzero.append(nz_min_prob)
		count_min_nonzero.append(nz_min_count)
		#plt.hist(counts[i*10:(i+1)*10])
		#plt.show()


	fig = plt.figure()
	#fig.suptitle("Neighbor sampling first 12h", fontsize=20)
	fig.suptitle(file, fontsize=20)

	plt.xlabel("Seconds after Tweet", fontsize=18)
	#plt.ylabel("Retweets", fontsize=18)

	#plt.plot(range(0,12), sample_prob_avgs_nonzero, lw = 1, label = 'Nonzero sample prob avg')
	#plt.plot(range(0,12), sample_prob_avgs, lw = 1, label = 'Sample prob avg')
	#plt.plot(range(0,12), prob_maxs, lw = 1, label = 'Max prob')
	#plt.plot(range(0,12), prob_min_nonzero, lw = 1, label = 'Min nonzero prob')

	#plt.plot(range(0,12), nonzeros, lw = 1, label = 'Percent Nonzero')

	plt.plot(range(0,hours), sample_count_avgs_nonzero, lw = 1, label = 'Nonzero sample count avg')
	plt.plot(range(0,hours), sample_count_avgs, lw = 1, label = 'Sample count avg')
	plt.plot(range(0,hours), count_maxs, lw = 1, label = 'Max count')
	plt.plot(range(0,hours), count_min_nonzero, lw = 1, label = 'Min nonzero count')

	plt.legend(loc = 'upper left')

	plt.show()
 
''' 
graph_probs('nk_12h_10.txt',12)
graph_probs('russia_12h_10.txt',12)
graph_probs('is_12h_10.txt',12)
graph_probs('nye_12h_10.txt',12)
graph_probs('maga_12h_10.txt',12)
'''
