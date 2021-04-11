import pandas as pd
import json

def get_stock_value(key):
    df=pd.read_csv("products.csv")
    product=df.loc[df['name']==key]
    return product.iloc[0]['quantity']


def item_in_inventory(key):
    df=pd.read_csv("products.csv")
    product=df.loc[df['name']==key]
    if product.empty:
        return 0;
    return 1;

def cart_total(cart,update_inventory):
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
             prod_df.loc[prod_df['name']==key,'quantity']=prod_df.loc[prod_df['name']==key,'quantity']-val;
    print("%20sTotal =>%8d" %('',total));
    if update_inventory:
        prod_df.to_csv("products.csv",index=False)
