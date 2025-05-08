from source.modules import *

class MD5:
    def __init__(self):
        md50 = hashlib.md5(open("./config.bin","rb").read()).hexdigest()
        md51 = hashlib.md5(open("./config_mod.bin","rb").read()).hexdigest()
        
        if md50 == md51:
            print(f"config.bin ::: {md50}")
            print(f"config_mod.bin ::: {md51}")
            print("Config Mod Is Valid!")
        else:
            print("Config Mod Not Is Valid!")
            print(f"config.bin: {md50} || config_mod.bin: {md51}")