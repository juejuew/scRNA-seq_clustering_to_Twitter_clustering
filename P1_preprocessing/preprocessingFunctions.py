#########################################################################
# #######################################################################
# ############   supplementary Functions for preprocessing # ############
# #######################################################################
# #######################################################################

## Packages need for data pre-process
import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

from scipy import sparse
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist

# word normalization (remove duplicate letters (e.g. llllooooovvvveee -> love))
nltk.download('wordnet')
import re
from nltk.corpus import wordnet
from repeatedReplacer import RepeatReplacer 
replacer = RepeatReplacer()

import itertools
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)


# This function is used to check whether the normalized words are in the wordnet or not
# Input: a string 
# Output: This function returns the normalized words if they are in their correct forms, 
# and returns the original word if the normalized words are not in correct forms

def check_replace(word):
    word_change = replacer.replace(word)
    if wordnet.synsets(word_change):
        return word_change
    else:
        return word
    
# Define basic pre-process function 
# Input: a string (original tweet)
# Output: a tring (pre-processed tweet)
def preProcessingFcn(tweet,removeAt=True, removeHashtags=True, removeNewline=True, removeURL=True, 
    removeNumbers=True, removeRepeated=True):
    
    tweet = re.sub(r"q&amp;a", " ", tweet)
    tweet = re.sub(r"&amp", " ", tweet)
    tweet = re.sub(r"can\'t", "can not", tweet)
    tweet = re.sub(r"can\’t", "can not", tweet)
    tweet = re.sub(r"won\'t", "will not", tweet)
    tweet = re.sub(r"won\’t", "will not", tweet)
    tweet = re.sub(r"\'s", " is", tweet)
    tweet = re.sub(r"\’s", " is", tweet)
    tweet = re.sub(r"\'d", " would", tweet)
    tweet = re.sub(r"\’d", " would", tweet)
    tweet = re.sub(r"don\'t'", "do not", tweet)
    tweet = re.sub(r"don\’t'", "do not", tweet)
    
    if removeAt == True:
        tweet = re.sub("@", "", tweet)
    if removeHashtags == True:
        tweet = re.sub("#", "", tweet)
    if removeNewline == True:
        tweet = re.sub("\s+", " ", tweet)
    if removeURL == True:
        tweet = re.sub(r"http\S+", "", tweet)
    if removeNumbers == True:
        tweet = re.sub("\d+th", "", tweet)
        tweet=  ''.join(i for i in tweet if not i.isdigit())
    if removeRepeated == True:
        tweet = ' '.join([check_replace(word) for word in tweet.split()])
        
    return tweet


# Define a function for stemming
# Input: a string (original tweet)
# Output: a tring (stemmed tweet)

def stemming(tweet, stem=True):
    ps = PorterStemmer()

    if stem==True:
        tweet = ' '.join([ps.stem(word) for word in tweet.split()])
    return tweet

# Define a function to remove the words that appear in most of the tweets
# Input: (1) D_T_input: the document-term matrix where the entries are absolute frequency;
#        (2) percent: a threshold where words appear in >= the "percent" of tweets will be removed;
#        (3) data_input: a list (for tweets) of list of word tokens
# Output: (1) D_T_dict: a dictionary {word type: frequency} of remaining words;
#         (2) data_after: trimmed data_input;
#         (3) D_T_out: processed document-term matrix;
#         (4) empty_idx: the index of the empty tweets 

def trim_common(D_T_input, percent, data_input):
    D_T = D_T_input.copy()
    tweets_num_ori = D_T.shape[0]
    
    D_T_count = D_T > 0 
    D_T_dict = D_T_count.sum(axis=0).to_dict()
    trim = int(percent*D_T_count.shape[0]/100.0)
    
    # Find the most common words
    common_words = []
    for i in range(len(D_T_dict)):
        word = list(D_T_dict.keys())[i]
        count = list(D_T_dict.values())[i]
        if count >= trim:
            common_words.append(word)
    
    for key in common_words:
        del D_T_dict[key]
        
    D_T_after = D_T[list(D_T_dict.keys())]
    D_T_out = D_T_after.loc[(D_T_after.sum(axis=1) != 0), (D_T_after.sum(axis=0) != 0)]
    
    empty_doc = D_T_after.loc[(D_T_after.sum(axis=1) == 0),]
    empty_idx = list(empty_doc.index)
    
    tweets_num_after = D_T_out.shape[0]
    prop_keep = round((tweets_num_after/tweets_num_ori) * 100, 2)
    print("Proportion of remaining tweets w.r.t. original tweets: " + str(prop_keep) + "%")
    prop_removed = round(100 - prop_keep, 2)
    print("Proportion of removed tweets w.r.t. original tweets: " + str(prop_removed) + "%")
    
    # Select words to keep from the data
    words_to_keep = list(D_T_dict.keys())
    data = data_input.copy()
    for i, value in enumerate(data):
        data[i] = [i for i in value if i in words_to_keep]
    data_after = list(filter(None, data))
    
    return D_T_dict, data_after, D_T_out, empty_idx

# Define a function to remove a proportion of least frequent words 
# Input: (1) data_input: a list (for tweets) of list of word tokens; 
#        (2) percent: the percent of the least frequent words to be removed
# Output: (1) dict_words_keep: a dictionary {word type: frequency} of remaining words; 
#         (2) data_after: trimmed data_input; 
#         (3) empty_idx: the index of the empty tweets 

def trim_noise(data_input, percent):
    data = data_input.copy()
    tweets_num_ori = len(data)
    merged = list(itertools.chain.from_iterable(data))

    # calculate the term frequency
    c = Counter(merged)
    # sort by frequency
    c = {k: v for k, v in sorted(c.items(), key=lambda item: item[1], reverse=True)}
    
    # obtain the target words' frequency dictionary
    trim = int(percent*len(c)/100.0)
    words_to_keep = list(c.keys())[0:-trim]
    dict_words_keep = {words: c[words] for words in words_to_keep}
    
    # Select words to keep from the data
    for i, value in enumerate(data):
        data[i] = [i for i in value if i in words_to_keep] 
        
    # Get the index of the doc that are deleted
    empty_idx = []
    
    for i, value in enumerate(data):
        if any(value) == False:
            empty_idx.append(i)
          
    # Delete empty tweets after removal of noise words
    data_after = list(filter(None, data))
    tweets_num_after = len(data_after)
    
    # Calculate the proportion of tweets left
    prop_keep = round((tweets_num_after/tweets_num_ori) * 100, 2)
    print("Proportion of remaining tweets w.r.t. original tweets: " + str(prop_keep) + "%")
    
    # Calculate the proportion of tweets removed
    prop_removed = round(100 - prop_keep, 2)
    print("Proportion of removed tweets w.r.t. original tweets: " + str(prop_removed) + "%")
    
    return dict_words_keep, data_after, empty_idx

