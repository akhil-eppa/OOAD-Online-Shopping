import pandas as pd
class Admin:
        '''
        ID
        Username
        Password
        '''
        def __init__(self,id,uname,passwd):
                df=pd.read_csv("admin.csv")
                self.id=id
                self.uname=uname
                self.passwd=passwd
                print(df[df["id"]==id and df["uname"]==uname and df["passwd"]==passwd]]
