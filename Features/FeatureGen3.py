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

dataPath = "../data/intelligencefiles/"

for subdir, dirs, files in os.walk(dataPath):
    for file in files:
        pe = pefile.PE(os.path.join(subdir, file))
        feature = getMetaData(pe)
	