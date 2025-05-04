#!./env/bin/python3

from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util import Padding
from io import BytesIO
import struct
import zlib
import argparse
from data import infile_bytes


class ZTE_TOOLS:
    def __init__(self):
        parser = argparse.ArgumentParser()
        
        parser.add_argument(
            "infile",
            type=argparse.FileType("rb"),
            help="arquivo de configuração config.bin"
        )
        parser.add_argument(
            "--serial",
            type=str,
            help="serial do seu roteador EX: ZTEXXXXXXXXX"
            )
        parser.add_argument(
            "--mac",
            type=str,
            help="Mac do seu roteador EX: XX:XX:XX:XX:XX:XX"
            )
        
        parser.add_argument(
            "--iv",
            type=str,
            help="IV do seu roteador"
            )
        parser.add_argument(
            "--op",
            type=argparse.FileType("rb"),
            help="--op repack para recompilar a config.bin ou --op unpack para descompilar a config.bin"
        )
        
        
        self.header = None
        self.hedaer_compress = None
        args = parser.parse_args()
        
        self.op = args.op
        self.serial = args.serial
        self.mac = args.mac
        self.aes_iv = args.iv
        self.infile = args.infile
        
        
    def gen_key(self):
        key_path_a = self.serial[-8:]
        key_path_b = ""
        mac_str = (str(self.mac).lower()).split(":")
        size_mac = len(mac_str)-1
        while True:
            key_path_b += mac_str[size_mac]
            size_mac-=1
            if size_mac == -1:
                break
        self.aes_key = key_path_a+key_path_b
    
    def save(self,name_path,data):
        data = data.read()
        if isinstance(data,bytes):
            data = bytes(data).decode()
        with open(name_path,"w") as f:
            f.write(str(data))
        
    
    def read_header(self):
        self.header = self.infile.read(206)
        self.infile.seek(206)
        print("Skip 206")
        
    def set_key(self):
        if isinstance(self.aes_key,str):
            self.aes_key = self.aes_key.encode()
                
        if self.aes_iv is None:
            self.aes_iv = self.aes_key
        elif isinstance(self.aes_iv,str):
            self.aes_iv = self.aes_iv.encode()
        
        key = sha256(self.aes_key).digest()
        iv = sha256(self.aes_iv).digest()
        self.aes_cipher = AES.new(key,AES.MODE_CBC,iv[:16])
            
            
    def decompress(self,infile):
        self.hedaer_compress = infile.read(60)
        
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
    
    def compress(self,infile):
        pass
        
    def load_chunk(self):
        enc_data = BytesIO()
        tt_dec_size = 0
        while True:
            try:
                dec_size,chunk_size,more_data = struct.unpack(">3I",self.infile.read(12))
            except:
                break
            enc_data.write(self.infile.read(chunk_size))
            tt_dec_size+=dec_size
            
            if more_data == 0:
                break
        enc_data.seek(tt_dec_size)
        
        return enc_data
    
    def decrypt(self):
        self.gen_key()
        self.set_key()
        data = self.load_chunk()
        data_size = data.tell()
        data.seek(0)
        res = BytesIO()
        res.write(self.aes_cipher.decrypt(data.read())[:data_size])
        res.seek(0)
        return res
    
    def encrypt(self):
        pass

if __name__ == "__main__":
    zTools = ZTE_TOOLS()
    zTools.read_header()
    data_compress = zTools.decrypt()
    res,_ = zTools.decompress(data_compress)
    zTools.save("config_decrypt.xml",res)
    