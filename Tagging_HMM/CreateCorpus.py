from __future__ import division
from nltk.corpus import conll2002
from collections import Counter
import pickle

train = conll2002.iob_words()
train_tags = [x[2] for x in train]
word_tag_count = Counter([(x[0],x[2]) for x in train])
tag_count = Counter(train_tags)

#calculate the conditional probability
from collections import Counter
import os
#because we're using the linear interpotation
#all trigram, bigram and unigram probabilities are needed here

trigrams, bigrams = [], []
# * => representing the start of the document
trigrams.append(('*', '*', train[0][2]))
trigrams.append(('*', train_tags[0], train_tags[1]))
i = 0
while i <= len(train_tags) - 3:
    trigrams.append((train_tags[i], train_tags[i+1], train_tags[i+2]))
    i += 1
trigram_counter = Counter(trigrams)

#same thing for bigram and unigram
bigrams.append(('*', train_tags[0]))
i = 0 
while i <= len(train_tags) - 3:
    bigrams.append((train_tags[i], train_tags[i+1]))
    i += 1
bigram_counter = Counter(bigrams)

unigram_counter = Counter(train_tags)

#pickle the file for later calculate the probabilities
file_names = os.listdir('./')
if 'unigram_counter.pkl' in file_names:
	print 'Unigram counter already exist.'
else:
	with open('./unigram_counter.pkl', 'w+') as f:
		pickle.dump(unigram_counter, f)
		print 'Unigram counter successfully saved.'

if 'bigram_counter.pkl' in file_names:
	print 'bigram counter already exist.'
else:
	with open('./bigram_counter.pkl', 'w+') as f:
		pickle.dump(bigram_counter, f)
		print 'bigram counter successfully saved.'

if 'trigram_counter.pkl' in file_names:
	print 'trigram counter already exist.'
else:
	with open('./trigram_counter.pkl', 'w+') as f:
		pickle.dump(trigram_counter, f)
		print 'trigram counter successfully saved.'

if 'word_tag_count.pkl' in file_names:
	pass
else:
	with open('./word_tag_count.pkl', 'w+') as f:
		pickle.dump(word_tag_count, f)

if 'tag_count.pkl' in file_names:
	pass
else:
	with open('./tag_count.pkl', 'w+') as f:
		pickle.dump(tag_count, f)

