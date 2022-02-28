import pefile
from ptrlib import *

key = b"FLAG" # flag works but FLAG is correct
pe = pefile.PE("FoxyFox.exe")

for rsrc in pe.DIRECTORY_ENTRY_RESOURCE.entries:
    for entry in rsrc.directory.entries:
        offset = entry.directory.entries[0].data.struct.OffsetToData
        size = entry.directory.entries[0].data.struct.Size
        encryptedImage = pe.get_memory_mapped_image()[offset:offset + size]
        img = xor(encryptedImage, key)
        with open("flag.png", "wb") as f:
            f.write(img)
        exit()
