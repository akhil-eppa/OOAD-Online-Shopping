import pandas as pd
class Customer:
        '''
        Username
        Password
        ID
        Name
        Address
        Contact
        '''
        def __init__(self,uname,password):
                df=pd.read_csv("users.csv")
                self.username=uname
                self.password=password
                print(df[df["username"]==uname and df["password"]==password])
                
c=Customer("aaa","aaa")
