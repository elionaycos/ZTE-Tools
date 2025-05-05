from source.modules import *
from source.zte_file import ZTE_FILE

class ZTE_ZLIB:
    def __init__(self):
        pass
        
    def decompress(self,infile):
        self.hedaer_compress = infile.read(60)
        ZTE_FILE("./data/header1.bin",self.hedaer_compress,binary=True).save()
        
        infile.seek(60)
        dec_data = BytesIO()
        crc = 0
        while True:
            aes_header = struct.unpack(">3I",infile.read(12))
            
            dec_length = aes_header[0]
            com_length = aes_header[1]
            com_chunk = infile.read(com_length)
            crc = zlib.crc32(com_chunk,crc)
            dec_chunk = zlib.decompress(com_chunk)
            assert dec_length == len(dec_chunk),"Error ao ler dados tamanho %i vs %i"%(dec_length,len(dec_chunk))
            dec_data.write(dec_chunk)
            if aes_header[2] == 0:
                break
        
        dec_data.seek(0)
        return (dec_data,crc)