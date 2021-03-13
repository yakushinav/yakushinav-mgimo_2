import random
import datetime

#подключаем библиотеку
import xml.dom.minidom as minidom

import pandas as pd

class xml_data:
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

    def get_data_from_xml(self, dom):
        pass

    def add_sample_data(self, count):
        pass


class category_table(xml_data):


    def get_data_from_xml(self, dom):

        pars = dom.getElementsByTagName(self.get_table_name())[0]

        # Читаем элементы таблицы
        nodes = pars.getElementsByTagName("item")

        # Выводим элементы таблицы на экран
        for node in nodes:
            id = node.getElementsByTagName("id")[0]
            name = node.getElementsByTagName("name")[0]
            parent = node.getElementsByTagName("parent")[0]
            self.add_item(int(id.firstChild.data), [name.firstChild.data, parent.firstChild.data])

    def add_sample_data(self, count):
        max_id=max(self.get_items().keys())+1
        for k in range(count):
            name=self.get_table_name()+str(k)
            parent=1
            self.add_item(max_id+k, [name, parent])



class dict_table(xml_data):


    def get_data_from_xml(self, dom):

        pars = dom.getElementsByTagName(self.get_table_name())[0]

        # Читаем элементы таблицы
        nodes = pars.getElementsByTagName("item")

        # Выводим элементы таблицы на экран
        for node in nodes:
            id = node.getElementsByTagName("id")[0]
            name = node.getElementsByTagName("name")[0]
            self.add_item(int(id.firstChild.data), [name.firstChild.data])

    def add_sample_data(self, count):
        max_id=max(self.get_items().keys())+1
        for k in range(count):
            name=self.get_table_name()+str(k)
            self.add_item(max_id+k, [name])

class customer_table(xml_data):


    def get_data_from_xml(self, dom):

        pars = dom.getElementsByTagName(self.get_table_name())[0]

        # Читаем элементы таблицы
        nodes = pars.getElementsByTagName("item")

        # Выводим элементы таблицы на экран
        for node in nodes:
            id = node.getElementsByTagName("id")[0]
            firstname = node.getElementsByTagName("firstname")[0]
            lastname = node.getElementsByTagName("lastname")[0]
            age = node.getElementsByTagName("age")[0]
            sex = node.getElementsByTagName("sex")[0]
            address = node.getElementsByTagName("address")[0]
            self.add_item(int(id.firstChild.data), [firstname.firstChild.data, lastname.firstChild.data,int(age.firstChild.data),sex.firstChild.data,int(address.firstChild.data)])

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

class product_table(xml_data):

    def get_data_from_xml(self, dom):

        pars = dom.getElementsByTagName(self.get_table_name())[0]

        # Читаем элементы таблицы
        nodes = pars.getElementsByTagName("item")

        # Выводим элементы таблицы на экран
        for node in nodes:
            id = int(node.getElementsByTagName("id")[0].firstChild.data)
            name = node.getElementsByTagName("name")[0].firstChild.data
            category_id = int(node.getElementsByTagName("category_id")[0].firstChild.data)
            price = int(node.getElementsByTagName("price")[0].firstChild.data)
            color_id = int(node.getElementsByTagName("color_id")[0].firstChild.data)
            size = node.getElementsByTagName("size")[0].firstChild.data
            season_id = int(node.getElementsByTagName("season_id")[0].firstChild.data)
            material_id = int(node.getElementsByTagName("material_id")[0].firstChild.data)
            self.add_item(id, [name, category_id, price, color_id, size, season_id, material_id])

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

class order_table(xml_data):


    def get_data_from_xml(self, dom):

        pars = dom.getElementsByTagName(self.get_table_name())[0]

        # Читаем элементы таблицы
        nodes = pars.getElementsByTagName("item")

        # Выводим элементы таблицы на экран
        for node in nodes:
            id = node.getElementsByTagName("id")[0]
            product_id = node.getElementsByTagName("product_id")[0]
            customer_id = node.getElementsByTagName("customer_id")[0]
            date = node.getElementsByTagName("date")[0]
            self.add_item(int(id.firstChild.data), [int(product_id.firstChild.data), int(customer_id.firstChild.data),date.firstChild.data])

    def add_sample_data(self, count, product_table, customer_table):
        max_id=max(self.get_items().keys())+1
        for k in range(count):
            product=random.choice(list(product_table.get_items().keys()))
            customer = random.choice(list(customer_table.get_items().keys()))
            date=datetime.date(random.randint(2017,2020),random.randint(1,12),random.randint(1,28))
            self.add_item(max_id+k, [product, customer, date])


class my_shop:
    def __init__(self, filename):
        # читаем XML из файла
        dom = minidom.parse(filename)
        dom.normalize()
        self.__caterogy = category_table("category")
        self.__caterogy.get_data_from_xml(dom)
        self.__city = dict_table("city")
        self.__city.get_data_from_xml(dom)
        self.__color = dict_table("color")
        self.__color.get_data_from_xml(dom)
        self.__customer = customer_table("customer")
        self.__customer.get_data_from_xml(dom)
        self.__material = dict_table("material")
        self.__material.get_data_from_xml(dom)
        self.__order = order_table("order")
        self.__order.get_data_from_xml(dom)
        self.__product = product_table("product")
        self.__product.get_data_from_xml(dom)
        self.__season = dict_table("season")
        self.__season.get_data_from_xml(dom)

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
