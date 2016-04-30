#!/usr/bin/env python 2.7
import os
import sys
import time
from StringIO import StringIO
from collections import defaultdict

import numpy as np
import pandas as pd
from pandas import (Series,DataFrame, Panel,)
from pprint import pprint
#from sklearn.metrics import precision_recall_fscore_support
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr

randn = np.random.randn

TRAIN = "train.csv"
TEST = "test.csv"
MOVIE = "../douban_user_movie.csv"
MUSIC = "../douban_user_music.csv"

"""
TODO:
1. Evaluation:
   Test data: select 10 ppl each with one book.
   predict: find the values of these 10 ppl with these books as vector.  
2. Build various paths: movie, music
2. Merge PTE scores
"""

class Recommend_book:
    """A recommendation system that gives one user and recommend book based on the simialrity between this user with other users"""
    def __init__(self, inputbook, inputmusic, inputmovie, weight55):
        """Given a list of userid, bookid, rating csv file, output the similarities between user and user through the meta-path 
           user-book-user (UBU), user-movie-user (UVU), or user-music-user(USU).
        """
        self.weight55 = weight55
        # build book matrix
        self.bookdf = pd.read_csv(inputbook)
        self.bookpivoted = self.bookdf.pivot(index='userid', columns='bookid', values='rating')
        print self.bookpivoted.shape
        # self.bookadj55 = self.bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0, 4.0], value=0.0).replace(to_replace=5.0, value=1.0)
#         self.bookadj45 = self.bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0], value=0.0).replace(to_replace=[4.0,5.0], value=1.0)
#         self.bookadj34 = self.bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 5.0], value=0.0).replace(to_replace=[3.0,4.0], value=1.0)
#         self.bookadj23 = self.bookpivoted.replace(to_replace=['NaN', 1.0, 4.0, 5.0], value=0.0).replace(to_replace=[2.0,3.0], value=1.0)
#         self.bookadj12 = self.bookpivoted.replace(to_replace=['NaN', 3.0, 4.0, 5.0], value=0.0).replace(to_replace=[1.0,2.0], value=1.0
#         self.UBU = self.build_user_similarity_matrix_UBU()
#         self.UBUB = self.build_user_similarity_matrix_UBUB()
        # build music matrix
        self.musicdf = pd.read_csv(inputmusic)
        self.musicpivoted = self.musicdf.pivot(index='userid', columns='musicid', values='rating')
        print self.musicpivoted.shape
        # self.musicadj55 = self.musicpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0, 4.0], value=0.0).replace(to_replace=5.0, value=1.0)
 #        self.musicadj45 = self.musicpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0], value=0.0).replace(to_replace=[4.0,5.0], value=1.0)
 #        self.musicadj34 = self.musicpivoted.replace(to_replace=['NaN', 1.0, 2.0, 5.0], value=0.0).replace(to_replace=[3.0,4.0], value=1.0)
 #        self.musicadj23 = self.musicpivoted.replace(to_replace=['NaN', 1.0, 4.0, 5.0], value=0.0).replace(to_replace=[2.0,3.0], value=1.0)
 #        self.musicadj12 = self.musicpivoted.replace(to_replace=['NaN', 3.0, 4.0, 5.0], value=0.0).replace(to_replace=[1.0,2.0], value=1.0)
 #        self.USU = self.build_user_similarity_matrix_USU()
 #        self.USUS = self.build_user_similarity_matrix_USUS()
        # build movie matrix
        self.moviedf = pd.read_csv(inputmovie)
        self.moviepivoted = self.moviedf.pivot(index='userid', columns='movieid', values='rating')
        print self.moviepivoted.shape
        # self.movieadj55 = self.moviepivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0, 4.0], value=0.0).replace(to_replace=5.0, value=1.0)
 #        self.movieadj45 = self.moviepivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0], value=0.0).replace(to_replace=[4.0,5.0], value=1.0)
 #        self.movieadj34 = self.moviepivoted.replace(to_replace=['NaN', 1.0, 2.0, 5.0], value=0.0).replace(to_replace=[3.0,4.0], value=1.0)
 #        self.movieadj23 = self.moviepivoted.replace(to_replace=['NaN', 1.0, 4.0, 5.0], value=0.0).replace(to_replace=[2.0,3.0], value=1.0)
 #        self.movieadj12 = self.moviepivoted.replace(to_replace=['NaN', 3.0, 4.0, 5.0], value=0.0).replace(to_replace=[1.0,2.0], value=1.0)
 #        self.UVU = self.build_user_similarity_matrix_UVU()
 #        self.UVUV = self.build_user_similarity_matrix_UVUV()

    #=============== Book ===================#
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
        
        UBU = self.weight55*self.bookadj55.dot(self.bookadj55.T) + self.bookadj45.dot(self.bookadj45.T) + \
            self.bookadj34.dot(self.bookadj34.T) + self.bookadj23.dot(self.bookadj23.T) + self.bookadj12.dot(self.bookadj12.T)
       
        print "===original pivoted matirx===="
        pprint (self.bookpivoted)
        # print "==adj55===="
        # pprint(self.bookadj55)
        # print "==adj55_dot===="
        # pprint(self.bookadj55.dot(self.bookadj55.T))
        # print "==adj45===="
        # pprint(self.bookadj45)
        # print "==adj45_dot===="
        # pprint(self.bookadj45.dot(self.bookadj45.T))
        # print "==adj34===="
        # pprint(self.bookadj34)
        # print "==adj34_dot===="
        # pprint(self.bookadj34.dot(self.bookadj34.T))
        # print "==adj12===="
        # pprint(self.bookadj12)
        # print "==adj12_dot===="
        # pprint(self.bookadj12.dot(self.bookadj12.T))
        # print "===UBU==="
        # pprint(UBU)
        return UBU
        
        
    def build_user_similarity_matrix_UBUB(self):
        UBUB = self.weight55*self.UBU.dot(self.bookadj55) + self.UBU.dot(self.bookadj45) + \
            self.UBU.dot(self.bookadj34) + self.UBU.dot(self.bookadj23) + self.UBU.dot(self.bookadj12)
        
        print "===UBUB===="
        pprint(UBUB)
        
        return UBUB   
    
    #=============== Music ===================#    
    def build_user_similarity_matrix_USU(self): 
        USU = self.weight55*self.musicadj55.dot(self.musicadj55.T) + self.musicadj45.dot(self.musicadj45.T) + \
            self.musicadj34.dot(self.musicadj34.T) + self.musicadj23.dot(self.musicadj23.T) + self.musicadj12.dot(self.musicadj12.T)
        return USU
    
    def build_user_similarity_matrix_USUS(self):
        USUS = self.weight55*self.USU.dot(self.musicadj55) + self.USU.dot(self.musicadj45) + \
            self.USU.dot(self.musicadj34) + self.USU.dot(self.musicadj23) + self.USU.dot(self.musicadj12)
        return USUS
        
    #=============== Movie ===================#    
    def build_user_similarity_matrix_UVU(self): 
        UVU = self.weight55*self.movieadj55.dot(self.movieadj55.T) + self.movieadj45.dot(self.movieadj45.T) + \
            self.movieadj34.dot(self.movieadj34.T) + self.movieadj23.dot(self.movieadj23.T) + self.movieadj12.dot(self.movieadj12.T)
        return UVU
    
    def build_user_similarity_matrix_UVUV(self):
        UVUV = self.weight55*self.UVU.dot(self.movieadj55) + self.UVU.dot(self.movieadj45) + \
            self.UVU.dot(self.movieadj34) + self.UVU.dot(self.movieadj23) + self.UVU.dot(self.movieadj12)
        return UVUV
             
        
def test(inputbook, train_matrix):
    """Compare the trained vectors with the test vectors to generate F1 score and p-value.
    """        
    testbookdf = pd.read_csv(inputbook)
    testrating_list = testbookdf['rating'].values.tolist()
    queryuser_list = testbookdf['userid'].values.tolist()
    querybook_list = testbookdf['bookid'].values.tolist()
    print "testrating_list: ", testrating_list
    size = len(queryuser_list)
    trainrating_list = []
    for i in range(0, size):
        user = queryuser_list[i]
        book = querybook_list[i]
        print user, book
        trainrating_list.append(train_matrix.at[user,book]) #rowid, colid
    print "trainrating_list: ", trainrating_list
    
    #compare the testrating_list & trainrating_list with pearson correlation and its p-value
    print "pearsonr: ", pearsonr(testrating_list, trainrating_list)
    
def main():
    start = time.time()
    
    r = Recommend_book("train.csv", "", "", 5.0)
    test("test.csv", r.UBUB)
    
    end = time.time()
    print (end-start)
    
    
if __name__ == "__main__":
    main()