import pefile

def ComputeHash(a,b):
	return hash(a+b)%256

filename = raw_input("Filename: ")

pe = pefile.PE(filename)

# If the PE file was loaded using the fast_load=True argument, we will need to parse the data directories:
pe.parse_data_directories()

feature2 = [0]*256

for entry in pe.DIRECTORY_ENTRY_IMPORT:
	# print entry.dll
	for imp in entry.imports:
		if imp.name != None:
			# print '\t', hex(imp.address), imp.name
			index = ComputeHash(entry.dll,imp.name)
			feature2[index] += 1
			
print feature2
