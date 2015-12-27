from tweepy import OAuthHandler
from tweepy import Stream
import json
from auth import TwitterAuth
import ssl
import time


import tweepy

auth = tweepy.OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

api = tweepy.API(auth)

if __name__ == '__main__':
   	text_file = open("suspected.txt", "r")
	try:
   	  for line in text_file:
    		parts = line.split('\t')
		print parts[0]
			
		try:
			user = api.get_user(parts[0])
		except tweepy.TweepError:#This exception will be triggered if the user has been suspended
			print ("suspended")
			fhSus = open("suspected","a")#Create a file to store output. "a" means append (add on to previous file)	
			fhSus.write(parts[1])
			fhSus.write("\t")
			fhSus.write(" is suspended")
			fhSus.write("\t")
			fhSus.write(parts[0])
			fhSus.write("\n")
			fhSus.close()
			continue
		print user.screen_name
		print user.followers_count
		if user.followers_count>1000:#we will collect the user whose followers are more than 1000. Collect their information later.
			fhPrt = open("huge","a")
			fhPrt.write(parts[1])
			fhPrt.write("\n")
			fhPrt.close()
			continue

		ids = []	
		try:
			for page in tweepy.Cursor(api.followers_ids, user_id=parts[0], count = 199).pages():
    				ids.extend(page)
				time.sleep(60) #set timeout, in order to avoid being stopped by twitter.
		except tweepy.TweepError:#This exception will be triggered if the user's profile is protected
			print ("protected\n")
			fhPrt = open("protected","a")
			fhPrt.write(parts[1])
			fhPrt.write("\n")
			fhPrt.close()
			continue
		fhOut = open("output","a")
		fhOut.write(parts[0])
		fhOut.write("\t")
		fhOut.write(parts[1])
		fhOut.write("\t\t")
		fhOut.write(" friends:")
		fhOut.write(str(user.followers_count))
		fhOut.write("\n")
		for i in xrange(0,len(ids),99):        #99 followers at a time
			for user in api.lookup_users(ids[i:i+99]):
				print user.screen_name
				fhOut.write("\t\t\t")
		    		fhOut.write(user.screen_name)
		    		fhOut.write("\n")	 
		fhOut.close()
		
		
	except KeyboardInterrupt:
	#User pressed ctrl+c -- get ready to exit the program
		pass
	text_file.close()
