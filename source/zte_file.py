class ZTE_FILE:
    def __init__(self,name_path,data,binary=False):
        self.name_path = name_path
        self.data = data
        self.binary = binary
    
    def save(self):
        if isinstance(self.data,bytes):
            print("ok")
        else:
            self.data = self.data.read()
            
        mod = "w"
        if self.binary:
            mod = "wb"
            if isinstance(self.data,str):
                self.data = bytes(self.data,"UTF-8")
        else:
            if isinstance(self.data,bytes):
                self.data = bytes(self.data).decode()
        
        print(self.name_path)
        print(mod)
        with open(self.name_path,mod) as f:
                f.write(self.data)