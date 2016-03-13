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


def build_user_similarity_matrix_UBU(filename, weight55):
    """Given a list of userid, bookid, rating csv file, output the similarities between user and user through the meta-path 
       user-book-user (UBU).
       As rating 4 and 5 are similar but not rating 3 and 5. So, we only build an adjacency matrix for two ratings that have
       less than one score difference: adj55,adj45,adj34,adj23,and adj12. As ratings that have a score of 5 should be more
       important than others, so we use a weight55 to put more weights on adj55.
       @param:  a csv filename
       @output: a user-user matrix where both the row and column are user ids; the value in the matrix position (i,j) are the 
                simialrity score between two users. The higher the value is, i and j are more similar.
    """
    bookdf = pd.read_csv(filename)
    bookpivoted = bookdf.pivot(index='userid', columns='bookid', values='rating')
    bookadj55 = bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0, 4.0], value=0.0).replace(to_replace=5.0, value=1.0)
    bookadj45 = bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0], value=0.0).replace(to_replace=[4.0,5.0], value=1.0)
    bookadj34 = bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 5.0], value=0.0).replace(to_replace=[3.0,4.0], value=1.0)
    bookadj23 = bookpivoted.replace(to_replace=['NaN', 1.0, 4.0, 5.0], value=0.0).replace(to_replace=[2.0,3.0], value=1.0)
    bookadj12 = bookpivoted.replace(to_replace=['NaN', 3.0, 4.0, 5.0], value=0.0).replace(to_replace=[1.0,2.0], value=1.0)

    UBU = weight55*bookadj55.dot(bookadj55.T) + bookadj45.dot(bookadj45.T) + bookadj34.dot(bookadj34.T) \
                                              + bookadj23.dot(bookadj23.T) + bookadj12.dot(bookadj12.T)
    print "===original pivoted matirx===="
    pprint (bookpivoted)
    print "==bookadj55===="
    pprint(bookadj55)
    print "==bookadj55_dot===="
    pprint(bookadj55.dot(bookadj55.T))
    print "==bookadj45===="
    pprint(bookadj45)
    print "==bookadj45_dot===="
    pprint(bookadj45.dot(bookadj45.T))
    print "==bookadj34===="
    pprint(bookadj34)
    print "==bookadj34_dot===="
    pprint(bookadj34.dot(bookadj34.T))
    print "==bookadj12===="
    pprint(bookadj12)
    print "==bookadj12_dot===="
    pprint(bookadj12.dot(bookadj12.T))
    
    return UBU

def main():
    UBU = build_user_similarity_matrix_UBU("book5.csv", 5.0)
    print "===PBP==="
    pprint(UBU)

if __name__ == "__main__":
    main()