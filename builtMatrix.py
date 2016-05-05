#!/usr/bin/python2.7


# *- remember: -* #
# 1. change the array size declared in cor_matrix(f1, f2)
# 2. change the input file for the purpose of building matrices
###############################################################


import numpy as np
import sys
from scipy.stats.stats import pearsonr
from tempfile import TemporaryFile

N_B = 147819
N_S = 237530
N_M = 56489
N_U = 42852
VEC_DIMENSION = 100

# return a dictionary id->idx
def id2idx(f):
	idx = 0;
	mapping = {}
	with open(f) as fp:
		for line in fp:
			sp = line.split()
			mapping[sp[0]] = idx
			idx += 1
	return mapping

# correlations
def cor_matrix(f1, f2):
	size1 = 0
	size2 = 0
	if f1 == 'ulist.txt':
		size1 = N_U
	elif f1 == 'blist.txt':
		size1 = N_B
	elif f1 == 'slist.txt':
		size1 == N_S
	elif f1 == 'mlist.txt':
		size1 == N_M
	else:
		print "check spelling"
		#return

	if f2 == 'ulist.txt':
		size2 = N_U
	elif f2 == 'blist.txt':
		size2 = N_B
	elif f2 == 'slist.txt':
		size2 == N_S
	elif f2 == 'mlist.txt':
		size2 == N_M
	else:
		print "check spelling"
		#return

	arr = [[0.1 for x in range(size2)] for y in range(size1)]

	with open(f1) as list1:
		list1_idx = 0
		for line1 in list1:
			sp1 = line1.rstrip().split()
			v1 = []
			for i in xrange(VEC_DIMENSION):
				v1.append(float(sp1[i+1]))

			list2_idx = 0
			
			with open(f2) as list2:
				for line2 in list2:
					sp2 = line2.rstrip().split()
					v2 = []
					for j in xrange(VEC_DIMENSION):
						v2.append(float(sp2[j+1]))
					#print v1
					#print v2
					#print pearsonr(v1, v2)
					arr[list1_idx][list2_idx] = pearsonr(v1, v2)[0]
							
					list2_idx += 1 
			# end for line2

			list1_idx += 1 
		# end for line1

	#return np.asmatrix(arr)
	return np.asmatrix(arr)


def main(argv):
	#blist = 'blist.txt'
	#book2idx_map = id2idx(blist)

	uu_matrix = cor_matrix(sys.argv[1], sys.argv[2])
	
	# save to file
	#np.savetxt('test_out.txt', uu_matrix)
	# binary file ended with .npy
	outfile = 'testout.npy'
	np.save(outfile, uu_matrix)

	# load the matrix from .npy file
	loadedMatrix = np.load(outfile)
	print(loadedMatrix)

	print "excited"
	# need to create matrices:
	# uu, ub, us, um
	# bb, bs, bm
	# ss, sm
	# mm

if __name__ == "__main__":
	main(sys.argv[1:])