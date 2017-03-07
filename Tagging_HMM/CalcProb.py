#First load in unigram, bigram and trigram counters
from __future__ import division
from collections import Counter
import os

def check_file(required_list):
	file_names = os.listdir('./')
	check_list = []
	for file in required_list:
		check_list.append(file in file_names)
	return all(check_list)

required_list = ['unigram_counter.pkl', 'bigram_counter.pkl', 'trigram_counter.pkl', 
		'word_tag_count.pkl', 'tag_count.pkl']

if not check_file(required_list):
	#pickle data
	os.system('python CreateCorpus.py')

#construct the conditional probability
#q(s|u,v) = W1 * q'(s|u,v) + W2 * q'(s|u) + W3 * q'(s)
#where q' is the maximum likelihood of q
#and W1 + W2 + W3 = 1
def _conditional_prob(trigram, unigram_counter, bigram_counter, trigram_counter, w1=0.6, w2=0.2, w3=0.2):
    trigram_total = sum(trigram_counter.values())
    bigram_total = sum(bigram_counter.values())
    unigram_total = sum(unigram_counter.values())
    
    trigram_prob = trigram_counter[trigram]/trigram_total
    bigram_prob = bigram_counter[(trigram[1], trigram[2])]/bigram_total
    unigram_prob = unigram_counter[trigram[2]]/unigram_total
    return w1 * trigram_prob + w2 * bigram_prob + w3 * unigram_prob

#calculating the emission probability
#probability of word given tag
#p(word|tag) = C(word,tag)/C(tag)  C => Count
def _emission_prob(word, tag, word_tag_count, tag_count):
	return word_tag_count[(word, tag)]/tag_count[tag]