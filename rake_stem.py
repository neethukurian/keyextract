#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrator
#
# Created:     29/07/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import RAKE
import operator
import string
import csv
import re
import itertools
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.util import bigrams,trigrams,ngrams
from collections import Counter

input_file='bcom_jd.txt'
key_score_file='bcom_keywords_stem.csv'

def text_clean(text):
    #exempt=list("'\/_.,()&")
    #punctuations=set(string.punctuation)-set(exempt)
    #text=filter(lambda x:(x in (set(string.printable)-punctuations)),text)
    text=filter(lambda x:(x in string.printable),text)
    text=re.sub('[!"#$%&\'\(\)*+,-/:;<=>?@[\]\^_`{|}~]',' ',text)
    text=text.replace('\n','.').strip()
    newtxt=""
    for line in nltk.sent_tokenize(text):
        if line[0].isdigit():
            line=line[2:].strip()
        newtxt=newtxt+line
    text=newtxt
    text=re.sub(' \.','.',text)
    text= re.sub('\.+','. ',text)
    text=re.sub(' +',' ',text)
    text=re.sub('&','and',text)

    text = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', text)
    text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
    text=re.sub(' +',' ',text)
    return(text)


def generate_unibitrigrams(key_score_file):
    with open(key_score_file,'rb') as infile:
        infile.readline()
        key_list=list()
        for line in infile:
            row=list(line.split(','))
            key_list.append(row[0])
    uni_bi_trigrams=[]
    for phrase in key_list:
        words=[]
        unigrams_ls=[]
        bigrams_ls=[]
        trigrams_ls=[]
        for word in nltk.word_tokenize(phrase):
            word=re.sub('[!"#$%&\'\(\)*+,-./:;<=>?@[\]\^_`{|}~]','',word)
            words.append(word)
        unigrams_ls=words
        #bigrams_ls=list(bigrams(words))

        for x in list(bigrams(words)):
            bigrams_ls.append(x[0]+' '+x[1] )


        for x in list(trigrams(words)):
            trigrams_ls.append(x[0]+' '+x[1]+' '+x[2] )
        #trigrams_ls=list(trigrams(words))
        uni_bi_trigrams=uni_bi_trigrams+unigrams_ls+bigrams_ls+trigrams_ls
    return uni_bi_trigrams


def main():

    rake=RAKE.Rake('SmartStoplist.txt')
    fp=open(input_file,'r')
    text=fp.read()
    text=text_clean(text)
    """wnl=WordNetLemmatizer()
    text=' '.join([wnl.lemmatize(i.strip()) for i in nltk.word_tokenize(text)])"""
    porter_stemmer=PorterStemmer()
    text=' '.join([porter_stemmer.stem(i.strip()) for i in nltk.word_tokenize(text)])
    keywords=rake.run(text)
   # print keywords

    with open(key_score_file,'wb') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['KEYWORD','SCORE'])
        for row in keywords:
            if row[1]>0:
                csv_out.writerow(row)


    unibitrigram_list=[]
    unibitrigram_list=generate_unibitrigrams(key_score_file)
    #print unibitrigram_list
    #ngram_freq=[]
    ngram_freq=Counter(unibitrigram_list)
    sorted_ngram_freq=sorted(ngram_freq.items(),key=lambda x:x[1],reverse=True )
    print ngram_freq
    with open('bcom_ngramfr_stem.csv','wb') as nf_csv:
        csv_wr=csv.writer(nf_csv)
        for item in sorted_ngram_freq:
            if ((item[0]!='')):
                csv_wr.writerow(item)



if __name__ == '__main__':
    main()
