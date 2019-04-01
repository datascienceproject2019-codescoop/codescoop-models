import pandas as pd
import numpy as np
import nltk
import operator
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

pd.set_option('display.max_columns', 500)

PATH ="/home/patrik/Desktop/Kurssit/DS_Project/repositories-1.2.0-2018-03-12/repositories-1.2.0-2018-03-12.csv"
dataRepo = pd.read_csv(PATH, nrows = 1000000, index_col=False)
dataRepo.head()
# build functions that we need for processing descriptions and data

# counting word frequencies
def words_freq(s):
    d={}
    for i in s.split():

        if i in d:
            d[i] +=1
        else:
            d[i] = 1
    return d

# converting variables to dummies
def getDummies (data, feature):
    dummies = pd.get_dummies(data[feature])
    data = pd.concat([data, dummies], axis=1)
    data = data.drop([feature],axis=1)
    return data

# get_neighbors returns k nearest neighbours for an instance
def get_neighbors(k, instance, data, labels):
    distances = []
    index = labels[labels == instance].index[0]
    inst = data.iloc[index]
    for i in range(len(data)):
        dist = np.linalg.norm(np.array(inst) - np.array(data.iloc[i]))
        distances.append((dist, i))
    distances.sort(key=lambda x: x[0])
    neighbors = distances[1:k+1]
    indexes = [x[1] for x in neighbors]
    return labels.iloc[indexes]

# findig keywords to use in knn

dataRepo.Keywords.fillna(0, inplace=True)
dataRepo.Description.fillna(0, inplace=True)
dataRepo = dataRepo[dataRepo['Stars Count'] !=0]
dataRepo = dataRepo[dataRepo.Description != 0]

descriptions = list(dataRepo.Description)

joinedDescriptions = " ".join(descriptions)
joinedDescriptions = joinedDescriptions.lower().translate(str.maketrans('', '', string.punctuation))
stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(joinedDescriptions)

filtered_sentence = [w for w in word_tokens if not w in stop_words]

filtered_sentence = []

for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

filtered_sentence = " ".join(filtered_sentence)

word_freq = words_freq(filtered_sentence)
sortedList = sorted(word_freq.items(), key = operator.itemgetter(1), reverse=True)
sortedDict = dict(sortedList)
top100 = list(sortedDict.keys())[:100]
print(top100)

# normalize numeric variables, should we weigh these somehow?
numeric_vars = ['Stars Count', 'Contributors Count', 'Forks Count']
knn_num = dataRepo[numeric_vars]
knn_num = knn_num.apply(lambda col: ((col-np.mean(col))/np.std(col)), axis=0)

# add dummies for language and keywords
knn_data = dataRepo[['Language', 'Description']]
knn_data = getDummies(knn_data, 'Language')

for word in top100:
    newcol = np.zeros(len(knn_data))
    i = 0;
    for row in knn_data['Description']:
        if(word in row):
            newcol[i] = 1
        i += 1
    knn_data[word] = newcol

# join numeric variables to knn data
knn_data[numeric_vars] = knn_num
knn_data = knn_data.drop(['Description'],axis=1)
knn_data.head()


names = dataRepo['Name with Owner']

# calculate k nearest neighbours for a project
nbrs = get_neighbors(5, "immense/knockout-pickatime", knn_data, names)
print(nbrs)
