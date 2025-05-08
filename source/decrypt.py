from source.modules import *
from source.zte_aes import ZTE_AES
from source.chunk import CHUNK
from source.zte_file import ZTE_FILE
from source.zte_zlib import ZTE_ZLIB


class DECRYPT:
    def read_header(self):
        self.header = self.infile.read(206)
        ZTE_FILE("./data/header0.bin",self.header,binary=True).save()
        self.infile.seek(206)
        
    def decrypt(self,aes_cipher,data):
        data_size = data.tell()
        data.seek(0)
        res = BytesIO()
        res.write(aes_cipher.decrypt(data.read())[:data_size])
        res.seek(0)
        return res
    
    def __init__(self,infile,serial,mac,iv):
        self.infile = infile
        self.read_header()
        
        aes = ZTE_AES(serial,mac,iv)
        
        zte_zlib = ZTE_ZLIB()
        
        aes_key = aes.get_key()
        
        cipher = aes.get_cipher(aes_key)
        
        chunk = CHUNK(self.infile)
        
        data_chunk = chunk.load_chunk()
                
        data_compress = self.decrypt(cipher,data_chunk)
        
        res,_ = zte_zlib.decompress(data_compress)
        
        ZTE_FILE("config.xml",res).save()
        
        print("Success in decompile Config.bin Output config.xml")
        
    