class ZTE_FILE:
    def __init__(self,name_path,data,binary=False):
        self.name_path = name_path
        self.data = data
        self.binary = binary
    
    def save(self):
        if isinstance(self.data,bytes):
            pass
        else:
            self.data = self.data.read()
            
        mod = "w"
        if self.binary:
            mod = "wb"
            if isinstance(self.data,str):
                self.data = bytes(self.data,"UTF-8")
        else:
            if isinstance(self.data,bytes):
                try:
                    self.data = bytes(self.data).decode()
                except:
                    self.data = bytes(self.data).decode("LATIN-1")
        with open(self.name_path,mod) as f:
                f.write(self.data)
    
    def open(self,name_path,binary):    
        mod = "r"
        if binary:
            mod = "rb"
        
        with open(name_path,mod) as f:
                data =  f.read(self.data)
        
        return data