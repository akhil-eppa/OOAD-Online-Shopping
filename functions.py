import pandas as pd
import json
import os

def get_stock_value(key):
    #returns stock value
    df=pd.read_csv("products.csv")
    product=df.loc[df['name']==key]
    return product.iloc[0]['quantity']


def item_in_inventory(key):
    #returns 1 if item in inventory, 0 otherwise
    df=pd.read_csv("products.csv")
    product=df.loc[df['name']==key]
    if product.empty:
        return 0;
    return 1;

def cart_total(cart,update_inventory):
    #update_inventory is set to 1 only during checkout
    #in which case it reduces inventory
    #set to 0 if just viewing the cart
    prod_df=pd.read_csv("products.csv")

    total=0;
    print("   Product  Quantity   Price  Amount");
    for key,val in cart.items():
         product=prod_df.loc[prod_df['name']==key]
         price=product.iloc[0]['price']
         amt=price*val

         total+=amt
         print("%10s%10s%8d%8d" %(key,val,price,amt))

         #reducing quantity in inventory
         if update_inventory:
             #print(prod_df.loc[prod_df['name']==key,'quantity']-val)
             prod_df.loc[prod_df['name']==key,'quantity']=prod_df.loc[prod_df['name']==key,'quantity']-val;

         #0 stock of item left in inventory, should clear out item from stock
         '''if update_inventory:
             stock=prod_df.loc[prod_df['name']==key,'quantity']-val
             print(type(stock))
             if stock:
                 prod_df.loc[prod_df['name']==key,'quantity']=stock
             else:
                prod_df.drop(prod_df[prod_df['name']==key].index,inplace=True);
            '''
    print("%20sTotal =>%8d" %('',total));

    if update_inventory:
    #updating the file
        prod_df.to_csv("products.csv",index=False)

def screen_clear():
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      _ = os.system('cls')
