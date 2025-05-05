#!./env/bin/python3

from source.modules import *
from source.decrypt import DECRYPT


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
            type=str,
            help="repack para recompilar a config.bin ou unpack para descompilar a config.bin"
        )
        
        args = parser.parse_args()
        
        self.serial = args.serial
        self.mac = args.mac
        self.aes_iv = args.iv
        self.infile = args.infile
        self.op = args.op 
        
        if self.op == "unpack":
            decrypt = DECRYPT(self.infile,self.serial,self.mac,self.aes_iv)
        
        elif self.op == "repack":
            pass
        
        else:
            print("Invalid Op")
            exit()
        





if __name__ == "__main__":
    ZTE_TOOLS()