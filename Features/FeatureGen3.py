'''
FeatureGen3.py

Author: Palash Chauhan
Last Updated: 19 Feb

Script to extract PE metadata features from
given binary execuatbles using pefile, a 
python PE file parser
'''

import pefile
import os


def getMetaData(pe):
	for section in pe.sections:
	   	print section.Name, hex(section.VirtualAddress), hex(section.Misc_VirtualSize), section.SizeOfRawData 


dataPath = "../data/intelligencefiles/"

for subdir, dirs, files in os.walk(dataPath):
    for file in files:
        pe = pefile.PE(os.path.join(subdir, file))
        feature = getMetaData(pe)
        break
        directory = subdir.replace("../data","3-metadata")
        if not os.path.exists(directory):
    		os.makedirs(directory)
		f = open(directory + "/meta_" + file, "w")
    	f.write(feature)
    	f.close()

	