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


def main():
    bookdf = pd.read_csv("book5.csv")
    bookpivoted = bookdf.pivot(index='userid', columns='bookid', values='rating')
    bookadj55 = bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0, 4.0], value=0.0).replace(to_replace=5.0, value=5.0)
    bookadj45 = bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 3.0], value=0.0).replace(to_replace=[4.0,5.0], value=1.0)
    bookadj34 = bookpivoted.replace(to_replace=['NaN', 1.0, 2.0, 5.0], value=0.0).replace(to_replace=[3.0,4.0], value=1.0)
    bookadj23 = bookpivoted.replace(to_replace=['NaN', 1.0, 4.0, 5.0], value=0.0).replace(to_replace=[2.0,3.0], value=1.0)
    bookadj12 = bookpivoted.replace(to_replace=['NaN', 3.0, 4.0, 5.0], value=0.0).replace(to_replace=[1.0,2.0], value=1.0)
    PBP = bookadj55+bookadj55
    #PBP = bookadj55.dot(bookadj55.T) + bookadj55.dot(bookadj55.T)
    print "===original pivoted matirx===="
    pprint (bookpivoted)
    print "==bookadj55===="
    pprint(bookadj55)
    print "==bookadj45===="
    pprint(bookadj45)
    print "==bookadj34===="
    pprint(bookadj34)
    print "==bookadj12===="
    pprint(bookadj12)
    print "===PBP==="
    pprint(PBP)
    
    


if __name__ == "__main__":
    main()