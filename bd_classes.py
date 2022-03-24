import random
import datetime

#подключаем библиотеку

import pandas as pd

class table_data:
    def __init__(self, table_name):
        self.__items={}
        self.__table_name=table_name


    def get_table_name(self):
        return self.__table_name

    def get_items(self):
        return self.__items

    def get_item(self, k):
        return self.__items[k]

    def add_item(self, key, value):
        self.__items[key]=value

    def print_items(self):
        for k in self.__items.keys():
            print(k, " ".join(map(str, self.__items[k])))

    def get_data_from_csv(self):
        pass

    def add_sample_data(self, count):
        pass


class category_table(table_data):

    def get_data_from_csv(self):
        df = pd.read_csv(self.get_table_name() + ".csv")
        for index, row in df.iterrows():
            self.add_item(row["id"], [row["name"], row["parent"]])


    def add_sample_data(self, count):
        max_id=max(self.get_items().keys())+1
        for k in range(count):
            name=self.get_table_name()+str(k)
            parent=1
            self.add_item(max_id+k, [name, parent])



class dict_table(table_data):


    def get_data_from_csv(self):
        df = pd.read_csv(self.get_table_name() + ".csv")

        for index, row in df.iterrows():
            self.add_item(row["id"], [row["name"]])

    def add_sample_data(self, count):
        max_id=max(self.get_items().keys())+1
        for k in range(count):
            name=self.get_table_name()+str(k)
            self.add_item(max_id+k, [name])

class customer_table(table_data):


    def get_data_from_csv(self):

        df = pd.read_csv(self.get_table_name() + ".csv")

        for index, row in df.iterrows():
            self.add_item(row["id"], [row["firstname"], row["lastname"],int(row["age"]),row["sex"],int(row["address"])])


    def add_sample_data(self, count, city_table):
        max_id=max(self.get_items().keys())+1
        for k in range(count):
            firstname="Иван"+str(k)
            lastname = "Иванов" + str(k)
            age=random.randint(18,90)
            if age%2==0:
                sex='F'
            else:
                sex = 'M'
            city=random.choice(list(city_table.get_items().keys()))
            self.add_item(max_id+k, [firstname, lastname, age, sex, city])

class product_table(table_data):

    def get_data_from_csv(self):
        df = pd.read_csv(self.get_table_name() + ".csv")

        for index, row in df.iterrows():
            self.add_item(row["id"],
                          [row["name"], int(row["category_id"]),
                           float(row["price"]), int(row["color_id"]),
                           row["size"],int(row["season_id"]),
                           int(row["material_id"])])


    def add_sample_data(self, count, category_table, color_table, season_table, material_table):
        max_id=max(self.get_items().keys())+1
        for k in range(count):
            name="Товар_"+str(k)
            category=random.choice(list(category_table.get_items().keys()))
            price = random.randint(100,1000)
            color = random.choice(list(color_table.get_items().keys()))
            size = random.choice(['S','M','L','XL','XXL'])
            season = random.choice(list(season_table.get_items().keys()))
            material = random.choice(list(material_table.get_items().keys()))

            self.add_item(max_id+k, [name, category, price, color, size, season, material])

class order_table(table_data):


    def get_data_from_csv(self):
        df = pd.read_csv(self.get_table_name() + ".csv")

        for index, row in df.iterrows():
            self.add_item(row["id"],
                          [int(row["product_id"]),
                           int(row["customer_id"]), row["date"]])

    def add_sample_data(self, count, product_table, customer_table):
        max_id=max(self.get_items().keys())+1
        for k in range(count):
            product=random.choice(list(product_table.get_items().keys()))
            customer = random.choice(list(customer_table.get_items().keys()))
            date=datetime.date(random.randint(2017,2021),random.randint(1,12),random.randint(1,28))
            self.add_item(max_id+k, [product, customer, date])


class my_shop:
    def __init__(self):
        # читаем XML из файла
        self.__caterogy = category_table("category")
        self.__caterogy.get_data_from_csv()
        self.__city = dict_table("city")
        self.__city.get_data_from_csv()
        self.__color = dict_table("color")
        self.__color.get_data_from_csv()
        self.__customer = customer_table("customer")
        self.__customer.get_data_from_csv()
        self.__material = dict_table("material")
        self.__material.get_data_from_csv()
        self.__order = order_table("order")
        self.__order.get_data_from_csv()
        self.__product = product_table("product")
        self.__product.get_data_from_csv()
        self.__season = dict_table("season")
        self.__season.get_data_from_csv()

    def add_sample_data(self, count):
        self.__caterogy.add_sample_data(count)
        self.__city.add_sample_data(count)
        self.__season.add_sample_data(count)
        self.__material.add_sample_data(count)
        self.__color.add_sample_data(count)
        self.__customer.add_sample_data(count, self.__city)
        self.__product.add_sample_data(count, self.__caterogy, self.__color, self.__season, self.__material)

    def add_sample_orders(self, count):
        self.__order.add_sample_data(count, self.__product, self.__customer)

    def getTrainingData(self):
        # Списки для хранения тренировочных данных
        pName = []
        pCategory = []
        pPrice = []
        pColor = []
        pSeason = []
        pMaterial = []
        cAge = []
        cSex = []
        cAddress = []

        for k in self.__order.get_items().keys():
            order=self.__order.get_item(k)
            pName.append( self.__product.get_item(order[0])[0])
            pCategory.append( self.__product.get_item(order[0])[1])
            pPrice.append( self.__product.get_item(order[0])[2])
            pColor.append( self.__product.get_item(order[0])[3])
            pSeason.append( self.__product.get_item(order[0])[5])
            pMaterial.append( self.__product.get_item(order[0])[6])
            cAge.append( self.__customer.get_item(order[1])[2])
            if self.__customer.get_item(order[1])[3]=='F':
                cSex.append(0)
            else:
                cSex.append(1)
            cAddress.append( self.__customer.get_item(order[1])[4])

        # Создаем фрейм данных

        df = pd.DataFrame(
                {'name': pName, 'category': pCategory, 'price': pPrice, 'color': pColor, 'season': pSeason,
                 'material': pMaterial, 'age': cAge, 'sex': cSex, 'address': cAddress})
        return df

    def print_color(self):
        self.__color.print_items()
