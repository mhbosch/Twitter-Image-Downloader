

''' 
A script that downloads all the pictures posted by a given user.

Author: Krishanu Konar
email: krishh_konar

'''

import os
import sys
import API_Tokens as t
import json
from tweepy import OAuthHandler, API, Stream
import wget
import requests


def main():
	#Authentication
	api = authenticate()
	path = str(os.getcwd()) + "\\twitter_images"
	print ('\n\nTwitter Image Downloader:\n========================\n')
	
	for eachArg in sys.argv:
		if eachArg == "--all":
			allusername = True
		else:
			allusername = False


	if allusername == True:
		for file in os.listdir(path):
			if os.path.isdir(path + file):
				print ("Hier ist kein Verzeichnis")
			else:
				print ("Nutze vorhandenen Usernamen " + file)
				all_tweets = getTweetsFromUser(file,0,api)
				media_URLs = getTweetMediaURL(all_tweets)
				downloadFiles(media_URLs,file)
	else:
		username = input("\nEnter the twitter handle of the Account to download media from: ")
		max_tweets = int(input("\nEnter Max. number of tweets to search (0 for all tweets): "))
		all_tweets = getTweetsFromUser(username,max_tweets,api)
		media_URLs = getTweetMediaURL(all_tweets)
		downloadFiles(media_URLs,username)
    
	print (r'Finished Downloading.')

def getTweetsFromUser(username,max_tweets,api):
	## Fetches Tweets from user with the handle 'username' upto max of 'max_tweets' tweets
	last_tweet_id, num_images = 0,0
	try:
	    raw_tweets = api.user_timeline(screen_name=username,include_rts=False,exclude_replies=True)
	except Exception as e:
		print (e)
		sys.exit()

	last_tweet_id = int(raw_tweets[-1].id-1)
	
	print ('\nFetching tweets.....')

	if max_tweets == 0:
		max_tweets = 3500

	while len(raw_tweets)<max_tweets:
		sys.stdout.write("\rTweets fetched: %d" % len(raw_tweets))
		sys.stdout.flush()
		temp_raw_tweets = api.user_timeline(screen_name=username, max_id=last_tweet_id, include_rts=False, exclude_replies=True)

		if len(temp_raw_tweets) == 0:
			break
		else:
			last_tweet_id = int(temp_raw_tweets[-1].id-1)
			raw_tweets = raw_tweets + temp_raw_tweets

	print ('\nFinished fetching ' + str(min(len(raw_tweets),max_tweets)) + ' Tweets.')
	return raw_tweets

def getTweetMediaURL(all_tweets):
	print('\nCollecting Media URLs.....')
	tweets_with_media = set()
	for tweet in all_tweets:
		media = tweet.entities.get('media',[])
		if (len(media)>0):
			tweets_with_media.add(media[0]['media_url'])
			sys.stdout.write("\rMedia Links fetched: %d" % len(tweets_with_media))
			sys.stdout.flush()
	print ('\nFinished fetching ' + str(len(tweets_with_media)) + ' Links.')

	return tweets_with_media

def downloadFiles(media_url,username):
	from pathlib import Path

	workdirectory = str(os.getcwd())
	print ('\nDownloading Images.....')
	try:
	    os.mkdir('twitter_images')
	    os.chdir('twitter_images')
	except:
		os.chdir('twitter_images')

	try:
	    os.mkdir(username)
	    os.chdir(username)
	except:
		os.chdir(username)

	for url in media_url:
		dateiname =  url.split("/")
		dateiname = (dateiname[len(dateiname)-1])
		fileName =  str(os.getcwd()) + "\\" + dateiname 
		fileObj = Path(fileName)
		if fileObj.is_file() == False:
			wget.download(url)
			print ("Lade Datei runter = " +url)
	
	os.chdir(workdirectory)


def authenticate():
	''' Authenticate the use of twitter API '''
	auth = OAuthHandler(t.CONSUMER_KEY, t.CONSUMER_SECRET)
	auth.set_access_token(t.ACCESS_TOKEN,t.ACCESS_TOKEN_SECRET)
	api = API(auth)
	return api


if __name__ == '__main__':
	main()
