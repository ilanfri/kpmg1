#!/usr/env/python

"""Compute the probability that a given document could be generated from a topic set (provided by LSI/LDA/...)"""

import enron
import stemming as stem
import cPickle as pickle


def importTopics(filename):
    topics_file = pickle.load(open(filename,'r'))
    topics =[]
    topicnumber=0
    for i in topics_file:
        for j in i:
            topics.append([topicnumber, str(j[1])])
        topicnumber+=1
    #print topics
    # The following removes word overlap between topics and leaves only unique words from all the topics. If this is not desired just return 'topics' instead
    found = set()
    for item in topics:
        if item[1] not in found:
            found.add(item[1])
    uniquetopics=list(found)
    #print uniquetopics
    return uniquetopics


def pofTgivenD(doc,topics):
    tokencount=1
    matchcount=0
    for i in doc:
        #print doc
        for j in topics:
            if i == j[1]:
                matchcount+=1
                #print "Match found for word {0} in topic {1}".format(i,j[0])
        tokencount+=1
    proboftopicgivendoc = float(matchcount)/float(tokencount)
    return proboftopicgivendoc




def main():

    #topics=importTopics('corpus_min1_stopwdsTrue_all_tfidf_lsi_topics.txt')
    topics=importTopics('test_corpus_lsi_topics.pkl')
    #print topics[0][0]

    con, cur=enron.connectDB("enron")

    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    tmp = [int(col) for row in res for col in row]
    size=tmp[0]

    #pofD=1./float(size)
    #pofT=1./10.

    for id in range(1,size):
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp = cur.fetchall()
        text_stem = stem.stemmingString(tmp[0][0], id, stopwords=True)
        #topicprob=pofTgivenD(text_stem,topics)*pofD/pofT 
        topicprob=pofTgivenD(text_stem,topics)     
        if topicprob>=1.: print "ERROR: PROBABILITY LARGER THAN 1"
        print "Probability of generating email {0} from this topic set: {1}".format(id,topicprob)
    con.close()




if __name__ == '__main__':
    main()
