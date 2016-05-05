#!usr/bin/python2.7

import numpy as np

# return a 2d array as logistic regression input
def logi (matrices):
	
	logi_in = []
	for matrix in matrices:
		logi_in.append(np.asarray(matrix.flatten())) # flatten and append

	return logi_in.T

def main(argv):
	matrices = []
	for i in range (1,len(sys.argv)):
		matrices.append(np.load(sys.argv[i]))

	# execute logi() somehow

if __name__ == '__main__':
	main(sys.argv[1:])
	

