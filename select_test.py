#!/usr/bin/env python 2.7
import os
import sys
import csv
import pandas as pd
import numpy as np
import random

FILELENGTH = 100
INFILE = "book100.csv"
OUTTRAIN = "trainbook100.csv"
OUTTEST = "testbook100.csv"
TESTLENGTH = 20
PERCENTAGE = 0.8

# reference: http://stackoverflow.com/questions/31112689/shuffle-and-split-a-data-file-into-training-and-test-set
def main():
    df = pd.read_csv(INFILE, header=0)
    filelength = (df.shape)[0] # df.shape = (#row, #col)
    shuffled_matrix = df.reindex(np.random.permutation(df.index))
    
    testlength = int(filelength*PERCENTAGE)

    headerlist = list(df.columns.values)
    shuffled_matrix[testlength:].to_csv(OUTTEST,header=headerlist, index=False)
    shuffled_matrix[:testlength].to_csv(OUTTRAIN,header=headerlist, index=False)

if __name__ == "__main__":
    main()