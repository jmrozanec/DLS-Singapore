import numpy as np
import os
from scipy.stats import entropy

def windowize(array, window_size, step_size, count):
        lower_bound = step_size*count
        higher_bound = lower_bound+window_size
        if(higher_bound<len(array)):
                return array[lower_bound:higher_bound]
        else:
                return []

def histo2d(filename, windowsize, offset):
	entropies = []
	bytez = []
	f = open(filename, "r")
	allbytes = np.fromfile(f, dtype=np.uint8) #http://stackoverflow.com/questions/1163459/reading-integers-from-binary-file-in-python int#, uint#, float#, complex#
	start=0
	
	while start<=(len(allbytes)-windowsize):
		window = windowize(allbytes, windowsize, offset, 0)
		probkeys, probvalues = np.unique(window, return_counts=True)
		entropymap = entropy(probvalues, probkeys, 2)
		entropies.extend(probvalues)
		bytez.extend(probkeys)
                start=start+offset

	H, xedges, yedges = np.histogram2d(bytez, entropies, bins=16, range=[[0, 255], [0, 8]], normed=False, weights=None)
	vector=[item for sublist in H for item in sublist]
	return vector
	
	
windowsize=1024.0
offset=256
samplesdir='/home/joze/other/repo/DLS-Singapore/dataset-india/intelligencefiles/20170105T114742/'
for filename in os.listdir(samplesdir):
	histo2d(samplesdir+filename, windowsize, offset)
