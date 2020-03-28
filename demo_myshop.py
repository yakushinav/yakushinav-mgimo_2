
from my_shop import MyShop
import pandas as pd

shop=MyShop("myShop.xml")
shop.print_materials()



shop.addSampleData(200,3,4)

shop.print_products()

df=shop.getTrainingData()
print(df)