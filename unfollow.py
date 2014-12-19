import twitter
import os
import mongo_db
import datetime
import pymongo
import random

CONSUMER_KEY = ''
CONSUMER_SECRET =''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                        CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

followers = set(twitter_api.followers.ids(screen_name=TWITTER_HANDLE)["ids"])
yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterday = yesterday.strftime("%Y_%m_%d")


unfollowfriends = set(user['id'] for user in mongo_db.load_from_mongo("twitter_bot", "friends", False, { "datetime": { "$lt": yesterday } }, None))
alreadyUnfollowedUsers = set(user['id'] for user in mongo_db.load_from_mongo("twitter_bot", "unfollowed_users", False, None, None))
unfollow_sf_friends = set(user['id'] for user in mongo_db.load_from_mongo("sf_bot", "san_francisco_friends", False, {"datetime": { "$lt": yesterday } }, None))
already_unfollowed_sf_users = set(user['id'] for user in mongo_db.load_from_mongo("sf_bot", "non_reciprocal_sf_users", False, None, None))
print already_unfollowed_sf_users
unfollowedUsers = []
unfollowed_sf_users = []
i=0
if len((unfollowfriends - alreadyUnfollowedUsers) - followers) == 0 or len((unfollow_sf_friends - already_unfollowed_sf_users) - followers) == 0 :
    print 'No users found.'
for userId in ((unfollow_sf_friends-already_unfollowed_sf_users)   - followers) :
	if unfollow_sf_friends != already_unfollowed_sf_users:
        
		twitter_api.friendships.destroy(user_id=userId)
		unfollowed_sf_users.append({"id": userId, "datetime": datetime.datetime.today()})
		print("unfollowed san francisco %d" % (userId))
		i += 1
		if i >10 :
                   break
j = 0	
for userId in ((unfollowfriends - alreadyUnfollowedUsers) - followers):
    twitter_api.friendships.destroy(user_id=userId)
    unfollowedUsers.append({"id": userId, "datetime": datetime.datetime.today()})
    print("unfollowed %d" % (userId))
    j += 1
    if j >= 5:
       break
       
mongo_db.save_to_mongo(unfollowedUsers, "twitter_bot", "unfollowed_users")
mongo_db.save_to_mongo(unfollowed_sf_users, "sf_bot", "non_reciprocal_sf_users")
