def windowize(array, window_size, step_size, count):
        lower_bound = step_size*count
        higher_bound = lower_bound+window_size
        if(higher_bound<len(array)):
                return array[lower_bound:higher_bound]
        else:
                return []

filename = '/home/joze/other/repo/DLS-Singapore/dataset-india/intelligencefiles/20170105T114742/14f74b7ba0b57dbb14d302997e0520b562527ccbd4aa9aff6feb86e47989380b'
windowsize=1024.0
import numpy as np

entropies = []
bytez = []
f = open(filename, "r")
allbytes = np.fromfile(f, dtype=np.uint8) #http://stackoverflow.com/questions/1163459/reading-integers-from-binary-file-in-python int#, uint#, float#, complex#

window = windowize(allbytes, windowsize, 256, 0)
probabilitymap = dict((x, window.count(x)/windowsize) for x in window)
entropymap = scipy.stats.entropy(probabilitymap.values(), probabilitymap.keys(), 2)
entropies.extend(entropymap.values())
bytez.extend(probabilitymap.keys())

histo2d = numpy.histogram2d(bytez, entropies, bins=16, range=[[0, 255], [0, 8]], normed=False, weights=None)

print(histo2d)

def windowize(array, window_size, step_size, count):
	lower_bound = step_size*count
	higher_bound = lower_bound+window_size
	if(higher_bound<len(array)):
		return array[lower_bound:higher_bound]
	else:
		return []

