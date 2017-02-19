import os
import signal
import subprocess
import sys

feature4 = [0]*1024

p = subprocess.Popen(['strings', 'test_files/malware.exe'], stdout=subprocess.PIPE)
for line in p.stdout.readlines():
	s = line.split('\n')[0]
	h = hash(s)%1024
	feature4[h] += 1

print feature4
