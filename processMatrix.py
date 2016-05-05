#!usr/bin/python2.7

import numpy as np
import sys

def getColumn(matrix, j):
	column_j = []
	for i in range (0, len(matrix)):
		column_j.append(matrix[i][j])
	return column_j

def id2idx(f):
	idx = 0;
	mapping = {}
	with open(f) as fp:
		for line in fp:
			sp = line.split()
			mapping[sp[0]] = idx
			idx += 1
	return mapping

# return all paths, in form of (ab, bc, cd) matrices
def readPath(file):
	pathList = []
	with open (file) as f:
		for line in f: # each line suggests a path
			line = line.rstrip()
			path = []
			for i in range(0, len(line) - 1):
				matrix = line[i] + line[i+1]
				path.append(matrix)
			pathList.append(path)

	return pathList

def readTestUser(file, mapping):
	userlist = []
	with open (file) as f:
		for line in f:
			line = line.rstrip()
			sp = line.split()
			for user in sp:
				userlist.append(mapping[user])
	return userlist

def readTestBook(file, mapping):
	booklist = []
	with open (file) as f:
		for line in f:
			line = line.rstrip()
			sp = line.split()
			for book in sp:
				booklist.append(mapping[book])
	return booklist

def multMatrix(path, test_uidx, test_bidx):
	um = [] # first matrix about test_u extracted from u matrix
	if len(path) == 1:
		#ub_whole = np.load('ub.npy')
		ub_whole = np.asmatrix(np.array([[1, 2], [3, 4], [5, 6]]))

		u1b = []
		u1b1 = []
		for i in test_uidx:
			u1b.append(np.squeeze(np.asarray(ub_whole[i])))
		for j in test_bidx:
			u1b1.append(getColumn(u1b, j))
		#u1b1 = np.array
		return np.asmatrix(zip(*u1b1))

	c0 = path[0][1] # character after first u
	cn = path[len(path - 1)][0] 

	# extract first and last matrix
	m0_whole = np.load('u' + c0 + '.npy')
	m0_arr = []
	for i in test_uidx:
		m0_arr.append(np.squeeze(np.asarray(m0_whole[i])))
	m0 = np.asmatrix(m0_arr)

	mn_whole = np.load(cn + 'b.npy')
	mn_arr = []
	for j in test_bidx:
		mn_arr.append(getColumn(np.asarray(mn_whole), j))
	mn = np.asmatrix(mn_arr)

	return m0.dot(mn)


def main(argv):
	uid2idx = id2idx('ulist.txt')
	bid2idx = id2idx('blist.txt')

	path = readPath(sys.argv[1])
	ulist = readTestUser(sys.argv[2], uid2idx)
	blist = readTestBook(sys.argv[3], bid2idx)
	#ulist = [0,1,2]
	#blist = [0]
	#print(multMatrix(path, ulist, blist))


if __name__ == "__main__":
	main(sys.argv[1:])