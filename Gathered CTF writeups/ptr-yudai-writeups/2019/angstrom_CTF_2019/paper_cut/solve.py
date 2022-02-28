from ptrlib import str2bytes
import zlib

with open("stream.bin", "rb") as f:
    buf = f.read()[2:]

while True:
    try:
        decoded = zlib.decompress(buf, -15)
        #print(decoded)
        break
    except zlib.error as e:
        buf += b'\xff'
        if "incomplete" in str(e):
            continue
        else:
            print(e)
            exit()
    
script = b'''%PDF-1.3\n'''
objpos = len(script)

# Something
script += b'''4 0 obj
<< /Length 5 0 R >>
stream
'''
script += decoded
script += b'''
endstream
endobj
'''

# Catalog
catalogpos = len(script)
script += b'''
1 0 obj
<<
/Pages 2 0 R
/Type /Catalog
>>
endobj
'''

# Page tree
pagetreepos = len(script)
script += b'''
2 0 obj
<<
/Kids [3 0 R]
/Count 1
/Type /Pages
>>
endobj
'''

# Page object
pageobjpos = len(script)
script += b'''
3 0 obj
<<
/Parent 2 0 R
/MediaBox [0 0 595 842]
/Contents 4 0 R
/Type /Page
>>
endobj
'''

# trailer
script += str2bytes('''xref
0 6
0000000000 65535 f 
{0:010} 00000 n 
{1:010} 00000 n 
{2:010} 00000 n 
{3:010} 00000 n 
trailer

<<
/Root 1 0 R
/Size 6
>>
startxref
{4}
'''.format(
    catalogpos,
    pagetreepos,
    pageobjpos,
    objpos,
    len(script)
))
script += b'%%EOF'

with open("repaired.pdf", "wb") as f:
    f.write(script)
