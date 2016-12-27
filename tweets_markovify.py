# twitter user name = @elonmusk

import markovify

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
access_key = "301847288-lWXEQAwNc7kvyIF4E6w3TCzj7FfWYyUs2FKXbkcR"
access_secret = "dXv1ktTNVsHVHsx7AUyVilLOx3tEWPc0Ffi8BvSh9VN10"
consumer_key = "MyrxJJIAAbIupjvNbqyUTzJOZ"
consumer_secret = "ZBZrMl7jEv1DGt76hCV60K7j8Z8uDx8K710cO1w6SBelNVSeqD"

# generate new texts
def markovify_text(string_path):
	# Get raw text as string.
	with open(string_path) as f:
	    text = f.read()

	# markov model
	text_model = markovify.Text(text)

	print '\nPossible sentences for user:\n'
	# random sentences
	for i in range(30):
	    print(text_model.make_sentence())
	    print '\n'

	print '\nPossible Tweets for user:\n'
	# something that he could tweet
	for i in range(30):
	    print(text_model.make_short_sentence(140))
	    print '\n'

# return path of stored tweets
def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	file_name = '%s_tweets.csv' % screen_name
	with open(file_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["text"])
		writer.writerows(outtweets)
	
	return file_name

# use get_all_tweets with user name to get a csv of tweets
# then call markovify_text to generate new texts
if __name__ == '__main__':
	#pass in the username of the account you want to download
	# string_path = get_all_tweets("elonmusk")
	string_path = 'elonmusk_tweets.csv'
	markovify_text(string_path)




