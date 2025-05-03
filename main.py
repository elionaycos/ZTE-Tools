#!.env/bin/python3

from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
from io import BytesIO
import struct
import zlib
import argparse


class ZTE_TOOLS:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "infile",
            type=argparse.FileType("rb"),
            help="arquivo de configuração config.bin"
        )
        parser.add_argument(
            "--key",
            type=str,
            help="Chave AES Do roteador"
            )
        
        args = parser.parse_args()
        
        self.key = args.key
        self.infile = args.infile
    
    def set_key(self):
        if not isinstance(self.key,bytes):
            aes_key = self.key.encode()
        else:
            aes_key = self.key
            
        aes_key = aes_key.ljust(16,b"\0")[:16]
        self.aes_cipher = AES.new(aes_key,AES.MODE_ECB)
    
    def decompress(self):
        dec_data = BytesIO()
        crc = 0
        while True:
            aes_header = struct.unpack(">3I",self.infile.read(12))
            if len(aes_header)<3:
                break
            
            dec_length = aes_header[0]
            com_length = aes_header[1]
            cum_length = aes_header[2]
            
            com_chunk = self.infile.read(com_length)
            if len(com_chunk) != com_length:
                print(f"Erro: Esperado {com_length} bytes, mas leu {len(com_chunk)} bytes")
                break
            
            crc = zlib.crc32(com_chunk,crc)
            try:
                dec_chunk = zlib.decompress(com_chunk)
            except zlib.error as e:
                print(e)
                break
            assert dec_length == len(dec_chunk), f"Erro: comprimento descomprimido não bate {dec_length} != {len(dec_chunk)}"
            
            dec_data.write(dec_chunk)
            if cum_length == 0:
                break
            
            dec_data.seek(0)
            return dec_data,crc
        
    def load_chunk(self):
        self.set_key()
        enc_data = BytesIO()
        tt_dec_size = 0
        while True:
            header = self.infile.read(12)
            if len(header) < 12:
                print("Invalid header")
                break
            
            c_size,d_size,m_chunks = struct.unpack(">3I",header)
            enc_data.write(self.infile.read(c_size))
            tt_dec_size += d_size
            if m_chunks == 0:
                break
            enc_data.seek(tt_dec_size)
            return enc_data
    
    def decrypt(self):
        data = self.load_chunk()
        data_size = data.tell()
        d = Padding.pad(data.read(),AES.block_size)
        data.seek(0)
        res = BytesIO()
        res.write(self.aes_cipher.decrypt(d))
        res.seek(0)
        return res

if __name__ == "__main__":
    zTools = ZTE_TOOLS()
    res = zTools.decompress()