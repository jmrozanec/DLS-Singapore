def padded_bin(number, width=8, padchar='0'):
    return bin(number)[2:].rjust(width, padchar)

with open('../data/intelligencefiles/20170105T114742/0a0c98cc7a2dc1fc27a977e7cd507504f9999921a53d4f5b78f638738826c978', 'rb') as f:
    as_binary = ''.join(padded_bin(ord(c)) for c in f.read())

print len(as_binary)