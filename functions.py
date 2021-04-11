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
        return 0
    return 1
