from nltk.corpus import names
import nltk
import random
import mongo_db
from nltk.classify import apply_features
import re
from matplotlib import pyplot as plt

def gender_features(word):
     return {'suffix1': word[-1:],
             'suffix2': word[-2:]}
             
names = ([(name, 'male') for name in names.words('male.txt')] +
          [(name, 'female') for name in names.words('female.txt')]) 
user_names = [user['id'] for user in mongo_db.load_from_mongo("project3", "reciprocal_user_features")]
random.shuffle(names)
featuresets = [(gender_features(n), g) for (n,g) in names]
train_set = apply_features(gender_features, names)
test_set2 = apply_features(gender_features, names[:500])
classifier = nltk.NaiveBayesClassifier.train(train_set)

print nltk.classify.accuracy(classifier, test_set2)

count = 0
for username in user_names:
    if username.startswith('San') or username.startswith('Francisco') or username.startswith('SF') or username.endswith('Francisco') or username.endswith('SF') :
            count +=1            
            user_names.remove(username)
print count            

   
re.sub(ur'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', u'', username)
for username in user_names:
      usernames_new.append(re.sub(ur'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', u'', username))
       
firstnames = []
for username_new in usernames_new:    
    firstnames.append(username_new.split())             
        
firstnames_new = []
for firstname in firstnames:
    firstnames_new.append(firstname[0])
    
gender = [] 
test_names = []   
for firstname_new in firstnames_new:
    test_names.append((firstname_new,classifier.classify(gender_features(firstname_new))))
    gender.append(classifier.classify(gender_features(firstname_new)))
       
test_set = apply_features(gender_features, test_names)

print nltk.classify.accuracy(classifier, test_set[:500])  
  
import csv

with open('non_rec_gender.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(gender)
male=[] 
female =[]   
with open('non_rec_gender.csv', 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar=',')
     for row in spamreader:
         for i in row:
             if i == 'male':
                 male.append(i)
             else:
                 female.append(i)
                
plt.figure(num=4, figsize=(18, 16))
plt.title('Reciprocal users', y=1.08)
labels = ['males', 'females', 'companies']

x=[len(male), len(female),count]
plt.pie(x, labels=labels,
   autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')

plt.show()
                 

        
