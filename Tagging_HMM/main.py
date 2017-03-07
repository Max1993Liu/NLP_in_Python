from __future__ import division
from CalcProb import _conditional_prob, _emission_prob
from UnseenWords import transform
from collections import Counter

import string
import pickle
import re
import os

file_names= os.listdir('./')
pkl_files = [file for file in file_names if file.endswith('.pkl')]
#load files
for file in pkl_files:
	with open(file, 'r+') as f:
		globals()[file[:-4]] = pickle.load(f)


#transform the word_count based on user-specific transformations
for k, v in word_tag_count.items():
	if v == 1:
		word_tag_count[(transform(k[0]), k[1])] = word_tag_count.pop(k)

#create functions to provide a simpler interface
def conditional_prob(trigram, w1=0.6, w2=0.2, w3=0.2):
	return _conditional_prob(trigram, unigram_counter, bigram_counter, trigram_counter, w1, w2, w3)

def emission_prob(word, tag):
	return _emission_prob(word, tag, word_tag_count, tag_count)
	


#using part of Alice's adventure in wonderland for testing
#TODO - parsing arguments for specifying input text

#two starting tags
starting_tags, prob = ['*', '*'], []
all_tags = tag_count.keys()
all_words = set([ k[0] for k in word_tag_count.keys()])

def clean_line(line, all_words):
	#TODO - better splitting with regrex
	#here we strip all punctuations
	line = line.strip().translate(None, string.punctuation)
	line  = line.split(' ')
	ret = []
	#if word not in training set, transform it
	for word in line:
		if word not in all_words:
			ret.append(transform(word))
		else:
			ret.append(word)
	#return both transformed and original list
	return ret, line

def viterbi(words, starting_tags, all_tags):
	#input a list of words
	#output list of ML tags
	s_tags, prob, ret = starting_tags, [], []
	for word in words:
		for tag in all_tags:
			temp_tag = tuple(s_tags + [tag])
			probability = conditional_prob(temp_tag) * emission_prob(word, tag)
			prob.append((tag, probability))
		#choose the tag with the highest probability
		prob = sorted(prob, key=lambda x: -x[1])
		next_tag = prob[0][0]
		ret.append(next_tag)
		s_tags = [s_tags[1]] + [next_tag]
	return ret

#straming file and tagging b line
tags, ret = ['*', '*'], []
with open('wonderland.txt', 'r+') as f:
	for line in f.readlines():
		line, original = clean_line(line, all_words)
		new_tags = viterbi(line, tags[-2:], all_tags)
		tags.extend(new_tags)
		ret.extend(zip(original, new_tags))

#line = clean_line(line, all_words)
#test =  viterbi(line, starting_tags, all_tags)
#print tags
print ret