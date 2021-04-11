'''

'''

import pandas as pd
import csv
import json
from csv import writer
from csv import reader
from functions import *

class User:
    def __init__(self, username, password,name,address,contact,email):
        self.username=username
        self.password=password
        self.name=name
        self.address=address
        self.contact=contact
        self.email=email

    def view_cart(self):
        with open('cart.csv','r') as file:
            csv_reader=csv.reader(file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1 # To skip header row
                else:
                    if row[1]==self.username:
                        usercart_dict=json.loads(row[2]) # JSON to Python
                        cart_total(usercart_dict,0)
                    line_count += 1
            file.close()

    def add_cart(self,key,value):
        usercart_dict=dict()
        line_count = 0
        with open('cart.csv','r') as file:
            csv_reader=csv.reader(file, delimiter=',')
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1 # To skip header row
                else:
                    line_count += 1 # To keep count of row number
                    if row[1]==self.username:
                        usercart_dict=json.loads(row[2]) #JSON to Python
                        if key in usercart_dict: # Check if product already present in cart
                            usercart_dict[key]+=value #Increase product count if already in cart
                        else:
                            usercart_dict[key]=value #Add product to cart
                        #print(usercart_dict)
            file.close()
        usercart_json=json.dumps(usercart_dict) #Python to JSON to save in updated csv
        df=pd.read_csv('cart.csv')
        df.loc[line_count-2,"cart_items"]=usercart_json #Update JSON string here
        df.to_csv("cart.csv",index=False)
        #print(df)
        print("Successfully Added Item To Cart!")

    def modify_cart(self,key,value):
        usercart_dict=dict()
        line_count = 0
        with open('cart.csv','r') as file:
            csv_reader=csv.reader(file, delimiter=',')
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1 # To skip header row
                else:
                    line_count += 1
                    if row[1]==self.username:
                        usercart_dict=json.loads(row[2]) #JSON to Python
                        if key in usercart_dict:
                            usercart_dict[key]=value #Update/Modify Value
                        else:
                            print("Item Not In Cart. Please Add In Cart In Order To Modify!")
            file.close()
        usercart_json=json.dumps(usercart_dict) #Python to JSON to save in updated csv
        df=pd.read_csv('cart.csv')
        df.loc[line_count-2,"cart_items"]=usercart_json #Update JSON string here
        df.to_csv("cart.csv",index=False)
        print("Successfully Modified Item In Cart!")

    def delete_cart(self):
        usercart_dict=dict()
        line_count = 0
        with open('cart.csv','r') as file:
            csv_reader=csv.reader(file, delimiter=',')
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1 # To skip header row
                else:
                    line_count += 1
                    if row[1]==self.username:
                        usercart_dict=json.loads(row[2]) #JSON to Python
                        usercart_dict.clear() #Clear dictionary
            file.close()
        usercart_json=json.dumps(usercart_dict) #Python to JSON to save in updated csv
        df=pd.read_csv('cart.csv')
        df.loc[line_count-2,"cart_items"]=usercart_json #Update JSON string here
        df.to_csv("cart.csv",index=False)
        print("Successfully Deleted Cart!")

    def display_products(self): # Replicated from Product_Management.py
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
            self.product_count=product_count-1 #To exclude header fields
            file.close()
    #add to class and change to self
    def w_add_item(self,key=-1):
        if key==-1:
            key=input("Enter The Name Of The Product You Wish To Add:")
            if not item_in_inventory(key):
                print("Item Not Present in Catalogue")
                print("Try Again\n")
                self.w_add_item()
                return
        value=int(input("Enter The Quantity You Wish To Add:"))
        if (value<=0):
            print("Please Enter A Quantity Greater than 0")
            self.w_add_item(key=key)
            return
        stock=get_stock_value(key)
        if value<=stock:
            self.add_cart(key,value)
        else:
            print (f'Only {stock} items available')
            print (f'Please try again with a number within the stock limit')
            self.w_add_item(key)

    #add to class and change to self
    def w_mod_item(self,key=-1):
        if key==-1:
            key=input("Enter The Name Of The Product You Wish To Modify:")
            if not item_in_inventory(key):
                print("Item Not Present in Catalogue")
                print("Try Again\n")
                self.w_mod_item()
                return
        value=int(input("Enter The Changed Quantity:"))
        if (value<=0):
            print("Please Enter A Quantity Greater than 0")
            self.w_add_item(key=key)
            return
        stock=get_stock_value(key)

        if value<=stock:
            self.modify_cart(key,value)
        else:
            print (f'Only {stock} items available')
            print (f'Please try again with a number within the stock limit')
            self.w_mod_item(key)

    def checkout(self):
        cart_df=pd.read_csv("cart.csv")
        user=cart_df.loc[cart_df['username']==self.username]
        cart=user.iloc[0]['cart_items']
        d_cart=json.loads(cart)
        if not d_cart:
            print("Cart is Empty, Checkout is not possible!")
            return
        #ensure all items are present in products
        #ensure all items are in stock
        checkout_fail=0 #
        for key,val in d_cart.items():
            if not item_in_inventory(key):
                print(f"{key} not present in inventory")
                checkout_fail=1
                continue
            stock=get_stock_value(key)
            if stock < val:
                print(f"Only {stock} units of '{key}' are present in inventory")
                checkout_fail=1
        if checkout_fail:
            return
        #generate billing
        cart_total(d_cart,1)
        self.delete_cart()


def main():
    df=pd.read_csv("users.csv")
    flag=1
    l_flag=0
    r_flag=0
    login_success=0
    while flag:
        try:
            print("Enter your choice\n1. Login\n2. Register\n")
            l=int(input("Choice:"))
        except:
            print("Invalid Format")
        if l==1:
            l_flag=1
            flag=0
        elif l==2:
            r_flag=1
            flag=0
        else:
            print("Incorrect Input")
    if r_flag:
        users=list(df[:]["username"])
        n=len(users)
        temp=1
        while (1):
            user=input("Enter Username:")
            if user=="exit":
                break
            if user in users: #Duplicate Username Condition
                print("Username Already Taken!")
                continue
            else: #Personal details
                user_passwd=input("Enter Password: ")
                name=input("Enter Name: ")
                address=input("Enter Address: ")
                contact=input("Enter Mobile Number: ")
                email=input("Enter Email Address: ")
                newuser_details=[str(n+1),user,user_passwd, name,address,int(contact),email]
                cart_dict={}
                cart_json=json.dumps(cart_dict)
                newuser_cartdetails=[str(n+1),user,cart_json] # For entry in cart.csv every time new registration is made
                with open('users.csv','a',newline='') as file:
                    writer_object=writer(file)
                    writer_object.writerow(newuser_details)
                    print("Registration Successful, Proceed to Login.\n\n")
                    file.close()
                with open('cart.csv','a',newline='') as file:
                    writer_object=writer(file)
                    writer_object.writerow(newuser_cartdetails)
                    file.close()
                l_flag=1
                break
    df=pd.read_csv("users.csv")
    while (l_flag):
        print("------User Login Portal---------")
        username=input("Enter username: ")
        password=input("Enter password: ")
        user_details=df['username'].values==username
        df_new=df[user_details]
        user_passwd=df_new['password'].values==password
        df_new=df_new[user_passwd]
        if len(df_new)!=0:
            print("User Login Successful!\n")
            l_flag=0
            login_success=1
        elif username=="exit":
            break
        else:
            print("Incorrect Credentials. Try Again!")

    login=login_success
    if login:
        Us=User(username,password,df_new['name'],df_new['address'],df_new['contact'], df_new['email'])
        while(login):
            print("\nWhat Do You Wish To Do?\n-------------------------")
            print("1. View Products\n2. View Cart\n3. Add Cart \n4. Modify Cart\n5. Delete Cart\n6. Checkout\n7. Logout")
            choice=int(input("Enter your choice: "))

            if choice==1:
                Us.display_products()

            elif choice==2:
                Us.view_cart()

            elif choice==3:
                Us.w_add_item()

            elif choice==4:
                Us.w_mod_item()

            elif choice==5:
                Us.delete_cart()

            elif choice==6:
                Us.checkout()

            elif choice==7:
                print("User Logged Out Successfully")
                login=0


if __name__=="__main__":
    main()
