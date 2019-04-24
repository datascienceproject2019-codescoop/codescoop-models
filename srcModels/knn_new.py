
import pandas as pd
import numpy as np
import nltk
import operator
import string
import spacy

from collections import Counter
from sklearn.neighbors import NearestNeighbors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nlp = spacy.load("en")
nltk.download('stopwords')
nltk.download('punkt')

pd.set_option('display.max_columns', 500)
PATH ="/home/patrik/Desktop/Kurssit/DS_Project/repositories-1.2.0-2018-03-12/repositories-1.2.0-2018-03-12.csv"
dataRepo = pd.read_csv(PATH, nrows = 500000, index_col=False)
dataRepo.head()

# build functions that we need for processing descriptions and data

# converting variables to dummies
def getDummies (data, feature):
    dummies = pd.get_dummies(data[feature])
    data = pd.concat([data, dummies], axis=1)
    data = data.drop([feature],axis=1)
    return data

def get_neighbors_improved(instance, data, labels):
    index = labels[labels == instance].index[0]
    inst = np.array(data[index]).reshape(1, -1)
    distances, indices = nbrs.kneighbors(inst)
    # loc OR iloc?
    return labels.iloc[indices[0]], np.round(distances, 3)

# processing the descriptions

dataRepo.Keywords.fillna(0, inplace=True)
dataRepo.Description.fillna(0, inplace=True)
dataRepo = dataRepo[dataRepo.Description != 0]

descriptions = list(dataRepo.Description)

stop_words = set(stopwords.words('english'))

# this takes forever
descr_lemmas = []
for element in descriptions:
    descr = [token.lemma_ for token in nlp(element) if token.is_stop != True and token.is_punct != True]
    descr = " ".join(descr)
    descr_lemmas.append(descr.lower())
dataRepo['Description'] = descr_lemmas

# for small data
'''
topWords = nlp(" ".join(descr_lemmas))
word_freq = Counter(topWords)
topWords = dict(word_freq.most_common(500)).keys()
'''

# for large data
empty = []
word_freq = Counter(empty)

for i in range(44):
    j = i*10000
    j2 = i*10000+10000
    if(j2 > len(descr_lemmas)):
        j2 = len(descr_lemmas)
    words = nlp(" ".join(descr_lemmas[j:j2]))
    word_freq += Counter(words)

topWords = dict(word_freq.most_common(500)).keys()

# Scale numeric variables using logarithms and normalization, this works well

numeric_vars = ['Stars Count', 'Contributors Count', 'Forks Count']
knn_num = dataRepo[numeric_vars]

knn_num = knn_num.apply(lambda col:((np.log(col+0.5)-np.mean(np.log(col+0.5)))/np.std(np.log(col+0.5))), axis=0)

# Check the distributions of numeric variables
'''
import matplotlib.pyplot as plt
import scipy.stats as scs
for var in numeric_vars:
    print(scs.describe(knn_num[var]))
    plt.hist(knn_num[var])
    plt.show()
'''
# add dummies for language and keywords
knn_data = dataRepo[['Language', 'Description']]
knn_data = getDummies(knn_data, 'Language')

knn_data.head()


for word in topWords:
    newcol = np.zeros(len(knn_data))
    i = 0;
    for row in knn_data['Description']:
        if(str(word) in row):
            newcol[i] = 0.25
        i += 1
    knn_data[word] = newcol

# join numeric variables to knn data
knn_data[numeric_vars] = knn_num
knn_data = knn_data.drop(['Description'],axis=1)
knn_data.head()

names = dataRepo['Name with Owner']

# DEMO

# Making a NN model, this takes a while but then retrieving info is very fast

knn_data = np.array(knn_data)
nbrs = NearestNeighbors(n_neighbors=11, algorithm='auto').fit(knn_data)

nbrsTEST, dists = get_neighbors_improved("immense/knockout-pickatime", knn_data, names)
nbrsTEST
dists

# Save model

#import pickle
#pickle.dump(nbrs, open('knn_model', 'wb'))
#np.save("/home/patrik/Desktop/Kurssit/DS_Project/knn_data.npy", knn_data)
#np.savetxt("/home/patrik/Desktop/Kurssit/DS_Project/knn_labes.csv", names, fmt='%s')
