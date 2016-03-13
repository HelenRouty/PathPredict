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
        self.UBU = self.build_user_similarity_matrix(self.bookpivoted)
        # build movie matrix
        # self.UMU = self.build_user_similarity_matrix_UBU(self.moviepivoted)

    def build_user_similarity_matrix(self, matrix):
        """Given a matrix, output the similarities between user and user through the meta-path in the given matrix: user-book-user,
           user-movie-user, or user-music-user.
           As rating 4 and 5 are similar but not rating 3 and 5. So, we only build an adjacency matrix for two ratings that have
           less than one score difference: adj55,adj45,adj34,adj23,and adj12. As ratings that have a score of 5 should be more
           important than others, so we use a weight55 to put more weights on adj55.
           @param:  a csv filename
           @output: a user-user matrix where both the row and column are user ids; the value in the matrix position (i,j) are the 
                    simialrity score between two users. The higher the value is, i and j are more similar.
        """
        adj55 = matrix.replace(to_replace=['NaN', 1.0, 2.0, 3.0, 4.0], value=0.0).replace(to_replace=5.0, value=1.0)
        adj45 = matrix.replace(to_replace=['NaN', 1.0, 2.0, 3.0], value=0.0).replace(to_replace=[4.0,5.0], value=1.0)
        adj34 = matrix.replace(to_replace=['NaN', 1.0, 2.0, 5.0], value=0.0).replace(to_replace=[3.0,4.0], value=1.0)
        adj23 = matrix.replace(to_replace=['NaN', 1.0, 4.0, 5.0], value=0.0).replace(to_replace=[2.0,3.0], value=1.0)
        adj12 = matrix.replace(to_replace=['NaN', 3.0, 4.0, 5.0], value=0.0).replace(to_replace=[1.0,2.0], value=1.0)

        UU = self.weight55*adj55.dot(adj55.T) + adj45.dot(adj45.T) + adj34.dot(adj34.T) + adj23.dot(adj23.T) + adj12.dot(adj12.T)
       
        print "===original pivoted matirx===="
        pprint (matrix)
        print "==adj55===="
        pprint(adj55)
        print "==adj55_dot===="
        pprint(adj55.dot(adj55.T))
        print "==adj45===="
        pprint(adj45)
        print "==adj45_dot===="
        pprint(adj45.dot(adj45.T))
        print "==adj34===="
        pprint(adj34)
        print "==adj34_dot===="
        pprint(adj34.dot(adj34.T))
        print "==adj12===="
        pprint(adj12)
        print "==adj12_dot===="
        pprint(adj12.dot(adj12.T))
    
        return UU

def main():
    r = Recommend_book("book5.csv", "", "", 5.0)
    pprint(r.UBU)
    
    # use pearsonr to obtain p-value
    print pearsonr([1,3,3],[2,3,3])

if __name__ == "__main__":
    main()