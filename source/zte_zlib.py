from source.modules import *
from source.zte_file import ZTE_FILE
from source.zte_aes import ZTE_AES

class ZTE_ZLIB:
    def __init__(self,serial,mac,aes_iv=None):
        self.zte_aes = ZTE_AES(serial=serial,mac=mac,aes_iv=aes_iv)
        
    def decompress(self,infile):
        hedaer_compress = infile.read(60)
        with open("datacom.txt","w") as f:
            f.write(str(infile.read()))
        infile.seek(60)
        
        ZTE_FILE("./data/header1.bin",hedaer_compress,binary=True).save()
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
        
        hedaer_compress = open("./data/header1.bin","rb")
        un_data = infile.read()
        
        un_length = len(un_data)
        
        #if un_length % 16> 0:
        #   data = data+(16-un_length%16)*b"\0"
        
        key =  self.zte_aes.get_key()
        aes_cipher = self.zte_aes.get_cipher(key)
        
        encry_data_len = len(aes_cipher.encrypt(pad(un_data, AES.block_size)))
        
        aes_header = struct.pack(
            ">3I",
            *(
                (
                encry_data_len
                if True
                else un_length
                ),
            ),
            encry_data_len,
            0,
        )
        
        data = BytesIO()
        com_data = BytesIO()
        
        
        data.write(hedaer_compress.read())
        data.write(struct.pack(">9I",*(9*[0])))
        data.write(aes_header)
        data.write(un_data)
        data.seek(0)
        
        com_data.write(zlib.compress(data.read()))
        com_data.seek(0)
        return com_data