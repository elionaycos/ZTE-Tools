from source.modules import *

class CHUNK:
    def __init__(self,infile):
        self.infile = infile
    
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