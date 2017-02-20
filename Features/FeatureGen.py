'''
FeatureGen.py

Author: Palash Chauhan
Last Updated: 19 Feb

Script to extract contextual byte features,
PE meta data and PE Import data from
given binary executables using pefile, a 
python PE file parser and 2dh
'''
import pickle
import pefile
import os, math, pickle
import numpy as np
from scipy.stats import entropy
import signal
import subprocess
import sys


def getStringHash(filename):
	feature = [0]*1024

	p = subprocess.Popen(['strings', filename], stdout=subprocess.PIPE)
	for line in p.stdout.readlines():
		s = line.split('\n')[0]
		h = hash(s)%1024
		feature[h] += 1
	return feature

def ComputeHash(a,b):
	return hash(a+b)%256


def getMetaData(pe):
	vec = [0]*256
	for i in pe.__structures__:
		if "FILE_HEADER" in i.name:
			for num in range(len(i.__keys__)):
				hsh = ComputeHash(i.__keys__[num][0], str(i.__unpacked_data_elms__[num]))
				vec[hsh] += 1
		if "OPTIONAL_HEADER" in i.name:
			for num in range(len(i.__keys__)):
				hsh = ComputeHash(i.__keys__[num][0], str(i.__unpacked_data_elms__[num]))
				vec[hsh] += 1
	return vec

def getImportData(pe):
	pe.parse_data_directories()
	vec = [0]*256
	for entry in pe.DIRECTORY_ENTRY_IMPORT:
		for imp in entry.imports:
			if imp.name != None:
				index = ComputeHash(entry.dll,imp.name)
				vec[index] += 1
	return vec

def myEntropy(freqList):
	ent = 0.0
	for freq in freqList:
	    if freq > 0:
	        ent = ent + freq * math.log(freq, 2)
	ent = -ent
	return ent

def getHistogram(filename):
	windowSize = 1024
	stepSize = 256
	E = []
	B = []
	L = 0
	U = 1024
	f1 = open(filename, "r")
	allbytes = np.fromfile(f1, dtype=np.uint8)
	while (U <= len(allbytes)):
		window = allbytes[L:U]
		probkeys, probvalues = np.unique(window, return_counts=True)
		probvalues = [values*1.0/1024 for values in probvalues]
		entropymap = myEntropy(probvalues)
		E.extend([entropymap]*1024)
		B.extend(window)
		L += 256
		U += 256
	histo2d = np.histogram2d(B, E, bins=16, range=[[0, 255], [0, 8]], normed=False, weights=None)
	vec = []
	for row in histo2d[0]:
		vec.extend(row)
	f1.close()
	return vec



dataPath = "../data/intelligencefiles/"


i = 1

for subdir, dirs, files in os.walk(dataPath):
	for file in files:
		try:
			pe = pefile.PE(os.path.join(subdir, file), fast_load = True)
			feature1 = getMetaData(pe)
			feature1 = [num*1.0/sum(feature1) for num in feature1]
			feature2 = getImportData(pe)
			feature2 = [num*1.0/sum(feature2) for num in feature2]
			feature0 = getHistogram(os.path.join(subdir, file))
			feature0 = [num*1.0/sum(feature0) for num in feature0]
			feature3 = getStringHash(os.path.join(subdir, file))
			feature3 = [num*1.0/sum(feature3) for num in feature3]
			feature = feature0 + feature2 + feature1 + feature3
			feature = [num*1.0/sum(feature) for num in feature]
			feature = [str(f) for f in feature]
			s = ",".join(feature)
			f = "fts/" + str(i)+"_feat.txt"
			ff = open(f,"w")
			ff.write(s)
			ff.close()	
			i+=1
			print file
		except:
			print "\t", file

		

	
		




	
