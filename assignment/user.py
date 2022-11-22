class User:
    def __init__(self):
        self.user_name = ''
        self.password = ''
        self.IP = ''
        self.port = ''
    
    def get_info(self):
        return {"user_name" : self.user_name,
                "password" : self.password}
    
    def get_ip(self):
        return self.IP
    
    def get_port(self):
        return self.port
    
    def set_ip(self,new_ip):
        self.IP = new_ip
    
    def set_port(self,new_port):
        self.port = new_port