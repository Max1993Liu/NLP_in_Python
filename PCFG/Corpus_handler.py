from nltk.corpus import treebank
import numpy as np
import pandas as pd

corpus_list = treebank.fileids()

sents = treebank.parsed_sents(corpus_list[1])[0]