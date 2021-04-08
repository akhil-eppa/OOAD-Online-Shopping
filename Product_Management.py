# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 15:46:35 2021

@author: Akhil
"""
import pandas as pd
import csv
from csv import writer
from csv import reader
class Admin:
    def __init__(self, username, password):
        self.username=username
        self.password=password
        
    def display_products(self):
        with open('products.csv') as file:
            csv_reader=csv.reader(file, delimiter=',')
            product_count=0
            for row in csv_reader:
                if product_count!=0:
                    print(f'Serial number {product_count}')
                    print(f'Product ID -> {row[0]}')
                    print(f'Product Name -> {row[1]}')
                    print(f'Current Product Quantity -> {row[2]}')
                    print(f'Product Price -> {row[3]}')
                    print(f'Product Seller -> {row[4]}\n')
                product_count+=1
            self.product_count=product_count-1#To exclude header fields
            file.close()
            
    def add_product(self, name, qty, price, seller):
        self.product_count+=1
        content=[self.product_count, name, qty, price, seller]
        with open('products.csv','a',newline='') as file:
            writer_object=writer(file)
            writer_object.writerow(content)
            file.close()
            
    def delete_product(self, num):
        if num<=0 or num>self.product_count:
            print("Wrong serial number entered!")
        else:
            updated_content=[]
            product_count=0
            with open('products.csv','r') as file:
                for row in csv.reader(file):
                    if product_count!=num:
                        updated_content.append(row)
                    product_count+=1
                file.close()
            print(updated_content)
            with open('products.csv','w',newline='') as file:
                writer_object=writer(file)
                for row in updated_content:
                    writer_object.writerow(row)
                file.close()
            self.product_count-=1
            print("Successfully deleted product from Catalogue. ")
            
    def modify_product(self, num):
        if num<=0 or num>self.product_count:
            print("Wrong serial number entered!")
        else:
            df=pd.read_csv("products.csv")
            flag=1
            while(flag):
                print(chr(27) + "[2J")
                print("\n----------\n1. Modify Product name\n2. Modify Product Quantity\n3. Modify Product Price\n4. Modify Seller name\n5. Confirm Modifications")
                try:
                    c=int(input("Enter your choice:"))
                except:
                    print("Invalid Format")
                    continue
                if c==1:
                    val=input("Enter updated value:")
                    df.loc[num-1,"name"]=val
                elif c==2:
                    try:
                        val=int(input("Enter updated value:"))
                    except:
                        print("Invalid Format")
                        continue
                    df.loc[num-1,"quantity"]=str(val)
                elif c==3:
                    try:
                        val=int(input("Enter updated value:"))
                    except:
                        print("Invalid Format")
                        continue
                    df.loc[num-1,"price"]=str(val)
                elif c==4:
                    val=input("Enter updated value:")
                    df.loc[num-1,"name"]=val
                elif c==5:
                    flag=0
                    df.to_csv("products.csv",index=False)
                    print("Modification Successful")
                else:
                    print("Invalid Choice")
def main():
    df=pd.read_csv("admins.csv")
    flag=1
    l_flag=0
    r_flag=0
    login_success=0
    while flag:
        try:
            print("Enter your choice\n1. login\n2. register\n3. exit")
            l=int(input("Choice:"))
        except:
            print("Invalid Format")
        if l==1:
            l_flag=1
            flag=0
        elif l==2:
            r_flag=1
            flag=0
        elif l==3:
            flag=0
        else:
            print("Incorrect Input")
    if r_flag:
        users=list(df[:]["username"])
        n=len(users)
        temp=1
        while (1):
            u=input("Enter username:")
            if u=="exit":
                break
            if u in users:
                print("Username already taken!")
                continue
            else:
                p=input("Enter password: ")
                content=[str(n+1),u,p]
                with open('admins.csv','a',newline='') as file:
                    writer_object=writer(file)
                    writer_object.writerow(content)
                    print("Registration Successful, Proceed to login.\n\n")
                    file.close()
                l_flag=1
                break
                
    #flag is use to keep repeating till login is successful
    df=pd.read_csv("admins.csv")
    while (l_flag):
        print("------Admin Portal---------")
        username=input("Enter username: ")
        password=input("Enter password: ")
        #First filter by given username
        #Create subset of data with the given username
        mask=df['username'].values==username
        df_new=df[mask]
        #In the subset of data check if password matches
        mask=df_new['password'].values==password
        df_new=df_new[mask]
        if len(df_new)!=0:
            print("Admin Login Successful!\n")
            l_flag=0
            login_success=1
            #Clear Terminal
            #print(chr(27) + "[2J")
        elif username=="exit":
            break
        else:
            print("Incorrect Credentials. Try Again!")
        
    login=login_success
    if login:
        Ad=Admin(username,password)
        Ad.display_products()
        while(login):
            print("\n-------------------------\n1. View Products\n2. Add Product\n3. Delete Product \n4. Modify Product\n5. Exit")
            choice=int(input("Enter your choice: "))
        
            if choice==1:
                Ad.display_products()
            elif choice==2:
                #print(chr(27) + "[2J")
                print("\n----Add Product-----")
                name=input("Enter product name: ")
                try:
                    qty=int(input("Enter product quantity: "))
                except:
                    print("Incorrect format")
                    continue
                try:
                    price=int(input("Enter product price: "))
                except:
                    print("Incorrect format")
                    continue
                seller=input("Enter seller name: ")
                Ad.add_product(name, qty, price, seller)
                print("Product Added successfully!\n")
            elif choice==3:
                Ad.display_products()
                try:
                    x=int(input("Enter serial number of product to be deleted: "))
                    Ad.delete_product(x)
                except:
                    print(chr(27) + "[2J")
                    print("Invalid Format!")
                
            elif choice==4:
                Ad.display_products()
                try:
                    x=int(input("Enter serial number of product to be modified: "))
                    Ad.modify_product(x)
                except:
                    print(chr(27) + "[2J")
                    print("Invalid Format!")
                    
            elif choice==5:
                login=0
            else:
                print(chr(27) + "[2J")
                print("Incorrect Choice")
        
    #print(df[df["username"]=="aa" and df["password"]=="aa"])

if __name__=="__main__":
    main()