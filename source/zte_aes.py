from source.modules import *

class ZTE_AES:
    def __init__(self,serial,mac,aes_iv):
        self.serial = serial
        self.mac = mac
        self.aes_iv = aes_iv
        self.key = None
    
    def get_key(self):
        key_path_a = self.serial[-8:]
        key_path_b = ""
        mac_str = (str(self.mac).lower()).split(":")
        size_mac = len(mac_str)-1
        while True:
            key_path_b += mac_str[size_mac]
            size_mac-=1
            if size_mac == -1:
                break
        aes_key = key_path_a+key_path_b
        return aes_key
    
    def get_cipher(self,aes_key):
        if isinstance(aes_key,str):
            aes_key = aes_key.encode()
                
        if self.aes_iv is None:
            self.aes_iv = aes_key
        elif isinstance(self.aes_iv,str):
            self.aes_iv = self.aes_iv.encode()
        
        key = sha256(aes_key).digest()
        iv = sha256(self.aes_iv).digest()
        aes_cipher = AES.new(key,AES.MODE_CBC,iv[:16])
        return aes_cipher
        