#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrator
#
# Created:     31/07/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    import string
    import csv
    import re
    import itertools
    from topia.termextract import tag
    tagger = tag.Tagger()
    tagger.initialize()
    fp=open('Mech.txt','r')
    text=fp.read()
    text=''.join(ch for ch, _ in itertools.groupby(text))
    text=filter(lambda x:(x in string.printable),text)
    #text=text.replace('\n','.')
    text=re.sub('[^a-zA-Z0-9.,;:\\/\'&()]',' ',text)

    print tagger.tokenize(text)
    print tagger(text)
    from topia.termextract import extract
    extractor = extract.TermExtractor()
    #extractor.filter = extract.permissiveFilter
    keywords= extractor(text)
    print keywords
    #print type(keywords)
    with open('topia_keywords.csv','wb')as tcsv:
        tcsv_write=csv.writer(tcsv)
        for row in sorted(keywords,key=lambda xrange:xrange[1]):
            tcsv_write.writerow(row)

if __name__ == '__main__':
    main()
