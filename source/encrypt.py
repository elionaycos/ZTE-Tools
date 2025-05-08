from source.modules import *
from source.zte_aes import ZTE_AES
from source.zte_zlib import ZTE_ZLIB
from datacom import databytes

class ENCRYPT:
    
    def write_header(self,infile):
        data = BytesIO()
        file = open("./data/header0.bin","rb")
        header0 = file.read()
        
        data.write(header0)
        data.write(infile.read())
        data.seek(0)
        
        return data
    
    def encrypt(self,aes_cipher,data):    
        res = BytesIO()
        res.write(aes_cipher.encrypt(pad(data.read(), AES.block_size)))
        res.seek(0)
        return res
    
    def __init__(self,infile,serial,mac):
        infile.seek(0)
        aes = ZTE_AES(serial=serial,mac=mac,aes_iv=None)
        zte_zlib = ZTE_ZLIB()
        
        data_compress = zte_zlib.compress(infile)
        
        key = aes.get_key()
        aes_chpher = aes.get_cipher(aes_key=key)
        data_enc = self.encrypt(aes_chpher,data_compress)
            
        data_enc_header =  self.write_header(data_enc)
        data_enc_header.seek(0)
        with open("config_mod.bin","wb") as f:
            f.write(data_enc_header.read())
        
        
        
        

