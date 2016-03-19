#!/usr/bin/env python 2.7
import os
import sys
from StringIO import StringIO
from collections import defaultdict

import numpy as np
import pandas as pd
from pandas import (Series,DataFrame, Panel,)
from pprint import pprint
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr

randn = np.random.randn

class Recommend_book:
    """A recommendation system that gives one user and recommend book based on the simialrity between this user with other users"""
    def __init__(self, inputbook, inputmovie, inputmusic, weight55):
        """Given a list of userid, bookid, rating csv file, output the similarities between user and user through the meta-path 
           user-book-user (UBU), user-movie-user (UVU), or user-music-user(USU).
        """
        self.weight55 = weight55
        # build book matrix
        self.bookdf = pd.read_csv(inputbook)
        self.bookpivoted = self.bookdf.pivot(index='userid', columns='bookid', values='rating')
        self.bookadj55 = self.bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0, 4.0], value=0.0).replace(to_replace=5.0, value=1.0)
        self.bookadj45 = self.bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0], value=0.0).replace(to_replace=[4.0,5.0], value=1.0)
        self.bookadj34 = self.bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 5.0], value=0.0).replace(to_replace=[3.0,4.0], value=1.0)
        self.bookadj23 = self.bookpivoted.replace(to_replace=['NaN', 1.0, 4.0, 5.0], value=0.0).replace(to_replace=[2.0,3.0], value=1.0)
        self.bookadj12 = self.bookpivoted.replace(to_replace=['NaN', 3.0, 4.0, 5.0], value=0.0).replace(to_replace=[1.0,2.0], value=1.0)
        
        self.UBU = self.build_user_similarity_matrix_UBU()
        self.UBUB = self.build_user_similarity_matrix_UBUB()
        # build movie matrix
        # self.UMU = self.build_user_similarity_matrix_UBU(self.moviepivoted)

    def build_user_similarity_matrix_UBU(self):
        """Given a matrix, output the similarities between user and user through the meta-path in the given matrix: user-book-user,
           user-movie-user, or user-music-user.
           As rating 4 and 5 are similar but not rating 3 and 5. So, we only build an adjacency matrix for two ratings that have
           less than one score difference: adj55,adj45,adj34,adj23,and adj12. As ratings that have a score of 5 should be more
           important than others, so we use a weight55 to put more weights on adj55.
           @param:  a csv filename
           @output: a user-user matrix where both the row and column are user ids; the value in the matrix position (i,j) are the 
                    simialrity score between two users. The higher the value is, i and j are more similar.
        """
        
        UU = self.weight55*self.bookadj55.dot(self.bookadj55.T) + self.bookadj45.dot(self.bookadj45.T) + \
            self.bookadj34.dot(self.bookadj34.T) + self.bookadj23.dot(self.bookadj23.T) + self.bookadj12.dot(self.bookadj12.T)
       
        #print "===original pivoted matirx===="
        #pprint (self.bookpivoted)
#         print "==adj55===="
#         pprint(self.bookadj55)
#         print "==adj55_dot===="
#         pprint(self.bookadj55.dot(self.bookadj55.T))
#         print "==adj45===="
#         pprint(self.bookadj45)
#         print "==adj45_dot===="
#         pprint(self.bookadj45.dot(self.bookadj45.T))
#         print "==adj34===="
#         pprint(self.bookadj34)
#         print "==adj34_dot===="
#         pprint(self.bookadj34.dot(self.bookadj34.T))
#         print "==adj12===="
#         pprint(self.bookadj12)
#         print "==adj12_dot===="
#         pprint(self.bookadj12.dot(self.bookadj12.T))
    
        return UU
        
    def build_user_similarity_matrix_UBUB(self):
        UBUB = self.weight55*self.UBU.dot(self.bookadj55) + self.UBU.dot(self.bookadj45) + \
            self.UBU.dot(self.bookadj34) + self.UBU.dot(self.bookadj23) + self.UBU.dot(self.bookadj12)
        
        #print "===UBUB===="
        #pprint(UBUB)
        
        return UBUB
        
        
def test(inputbook, train):
    """Compare the trained vectors with the test vectors to generate F1 score and p-value.
    """        
    testbookdf = pd.read_csv(inputbook)
    testlist = testbookdf['rating'].values.tolist()
    trainlist = []
    queryUserlist = testbookdf['userid'].values.tolist()
    queryBooklist = testbookdf['bookid'].values.tolist()

    print train
    for i in range(0, len(queryUserlist)):
        userid = []
        bookid = []
        i = 7
        userid.append(queryUserlist[i])
        bookid.append(queryBooklist[i])
        trainRating = train[userid][bookid] #rowid, colid
        print queryUserlist[i], queryBooklist[i]
        print trainRating
        trainlist.append(trainRating)
    #TODO: the above loop cannot find userid and bookid even if I use book100.csv for trainning.
    
    #print trainlist
        
    
def main():
    
    r = Recommend_book("trainbook100.csv", "", "", 5.0)
    test("testbook100.csv", r.UBUB)
    
    # use pearsonr to obtain p-value
    #print pearsonr([1,3,3],[2,3,3])
    #http://docs.scipy.org/doc/scipy/reference/stats.html
    
    # p-value
    # from sklearn.cross_validation import KFold
    # http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.KFold.html
    

if __name__ == "__main__":
    main()