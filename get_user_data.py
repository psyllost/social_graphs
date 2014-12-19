import twitter
import datetime
import random
import string
import json
import time
import csv
import basic_auth
import mongo_db
import twitter_request

def cleanUser(userData):
    cleanData = dict()
    cleanData['id'] = userData['id'] if 'id' in userData.keys() else None
    cleanData['id_str'] = userData['id_str'] if 'id_str' in userData.keys() else None
    cleanData['name'] = userData['name'] if 'name' in userData.keys() else None
    cleanData['description'] = userData['description'] if 'description' in userData.keys() else None
    cleanData['followers_count'] = userData['followers_count'] if 'followers_count' in userData.keys() else None
    cleanData['friends_count'] = userData['friends_count'] if 'friends_count' in userData.keys() else None
    cleanData['listed_count'] = userData['listed_count'] if 'listed_count' in userData.keys() else None
    cleanData['created_at'] = userData['created_at'] if 'created_at' in userData.keys() else None
    cleanData['favourite_count'] = userData['favourite_count'] if 'favourite_count' in userData.keys() else None
    cleanData['verified'] = userData['verified'] if 'verified' in userData.keys() else None
    cleanData['statuses_count'] = userData['statuses_count'] if 'statuses_count' in userData.keys() else None
    cleanData['protected'] = userData['protected'] if 'protected' in userData.keys() else None
    return cleanData

api = basic_auth.oauth_login()
ids_rec = []
with open('sf_reciprocal.csv', 'r') as csvfile:
    read = csv.reader(csvfile, delimiter=',',
                             quotechar=',',quoting=csv.QUOTE_MINIMAL)

    for row in read:
         ids_rec.extend(row)
ids_non_rec = []
with open('sf_non_reciprocal.csv', 'r') as csvfile:
    read2 = csv.reader(csvfile, delimiter=',',
                             quotechar=',',quoting=csv.QUOTE_MINIMAL)

    for row2 in read2:
         ids_non_rec.extend(row2)


span = 100
grouped_ids = [",".join(ids_non_rec[i:i+span]) for i in range(0, len(ids_non_rec), span)]

print "Found {0} groups of ids".format(len(grouped_ids))

savedUsers = set([user['id_str'] for user in mongo_db.load_from_mongo("project3", "non_reciprocal_user_features")])
i = 0
for group_id in grouped_ids:
    try:
        user_data = api.users.lookup(user_id=group_id, include_entities=False)
        for user in user_data:
            if user['id_str'] not in savedUsers:
                if user['protected'] == False:
                    mongo_db.save_to_mongo([cleanUser(user)], "project3", "non_reciprocal_user_features") 
    except Exception as e:
        print e
    except:
        print "Could not get details about this user group"
    
    i += 1
    if i % 14 == 0:
        print "Sleeping 20min"
        time.sleep(20*60)
