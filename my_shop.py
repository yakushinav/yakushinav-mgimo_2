#подключаем библиотеку
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import random
import pandas as pd

def prettify(elem):
    """Форматирование для получения читабельного XML.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='\t')


#Общий класс для хранения справочников material, season, color, address
class Catalog:
    def __init__(self, nodes):
        self.items = {}
        for node in nodes:
            id = node.getElementsByTagName("id")[0]
            name = node.getElementsByTagName("name")[0]
            self.items[int(id.firstChild.data)] = name.firstChild.data

    def add_item(self,id, name):
        self.items[id] = name

    def get_item(self, code):
        return self.items[code]

    def print_items(self):
        for k in self.items:
            print(k, self.items[k])

class Product:
    def __init__(self, node):
        # конструктор, создает экземпляр класса
        # читаем поля товара из узла XML

        self.name = node.getElementsByTagName("name")[0].firstChild.data
        self.category = int(node.getElementsByTagName("category_id")[0].firstChild.data)
        self.price = float(node.getElementsByTagName("price")[0].firstChild.data)
        self.color = int(node.getElementsByTagName("color_id")[0].firstChild.data)
        self.size = node.getElementsByTagName("size")[0].firstChild.data
        self.season = int(node.getElementsByTagName("season_id")[0].firstChild.data)
        self.material = int(node.getElementsByTagName("material_id")[0].firstChild.data)

    def print_product(self, material, season, color, category):
        m=material.get_item(self.material)
        print('({}, {}, {}, {}, {}, {}, {})'.format(self.name, category[self.category], self.price,
                                                  color[self.color], self.size,
                                                  season[self.season], material.get_item(self.material)))

class MyShop:
    def __init__(self, filename):
        # читаем XML из файла
        dom = minidom.parse(filename)
        dom.normalize()
        # Читаем таблицу Materials
        pars = dom.getElementsByTagName("material")[0]
        # Читаем элементы таблицы Materials
        nodes = pars.getElementsByTagName("item")
        self.materials = Catalog(nodes)

        # Читаем таблицу Product
        pars = dom.getElementsByTagName("product")[0]
        # Читаем элементы таблицы Product
        nodes = pars.getElementsByTagName("item")
        self.products={}
        for node in nodes:
            self.products[int(node.getElementsByTagName("id")[0].firstChild.data)]=Product(node)

        self.colors = {1: 'red', 2: 'black', 3: 'black', 4: 'black'}
        self.seasons = {1: 'winter', 2: 'summer', 3: 'black', 4: 'black'}
        self.categories = {1: 'dress', 2: 'boots', 3: 'coats', 4: 'some'}

    def print_materials(self):
        self.materials.print_items()

    def print_products(self):
        for k in self.products:
            self.products[k].print_product(self.materials, self.seasons, self.colors, self.categories)

    def addSampleData(self, nProd, nCustomer, nOrder):
        maxProd = max(self.products) + 1
        for i in range(nProd):
            dom=minidom.Document()
            elem=dom.createElement("item")
            elements={}
            elements["id"]=maxProd
            elements["name"]="Товар_"+str(i)
            elements["category_id"]=1 #категория товара (нужно будет выбрать случайно из категорий
            elements["price"]=random.randint(100,1000)
            elements["color_id"]=random.choice(list(self.colors))
            elements["size"]=random.choice(["M","L","S","XL","XS"])
            elements["season_id"]=random.choice(list(self.seasons))
            elements["material_id"] = random.choice(list(self.materials.items))

            for k in elements:
                field=dom.createElement(k)
                text = dom.createTextNode(str(elements[k]))
                field.appendChild(text)
                elem.appendChild(field)
            dom.appendChild(elem)
            self.products[int(elem.getElementsByTagName("id")[0].firstChild.data)] = Product(elem)
            maxProd = maxProd + 1  # номер следующего товара

    def getTrainingData(self):
        # Поскольку сейчас у нас нет заказов (не реализован шаг 3), то добавим просто случайные данные
        # если реализован этот шаг, то этот код нужно будет удалить
        order = {}
        for i in range(1500):
            order[i + 1] = [i + 1, random.choice(list(self.products)), random.randint(1, 30)]
        # Поскольку сейчас у нас нет клиентов (не реализован шаг 3), то добавим просто случайные данные
        # если реализован этот шаг, то этот код нужно будет удалить
        customer = {}
        for i in range(30):
            customer[i + 1] = [i + 1, random.randint(18, 65), random.choice([0, 1]),
                               random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])]

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

        # Проходим по всем заказам
        for i in order:
            # Выбираем из таблицы Товары товар по номеру из Заказа и добавляем поля в список
            pName.append(self.products[order[i][1]].name)
            pCategory.append(self.products[order[i][1]].category)
            pPrice.append(self.products[order[i][1]].price)
            pColor.append(self.products[order[i][1]].color)
            pSeason.append(self.products[order[i][1]].season)
            pMaterial.append(self.products[order[i][1]].material)
            # Выбираем из таблицы Клиенты клиента по номеру из Заказа и добавляем поля в список
            cAge.append(customer[order[i][2]][0])
            cSex.append(customer[order[i][2]][1])
            cAddress.append(customer[order[i][2]][2])
        # Создаем фрейм данных
        df = pd.DataFrame({'name': pName, 'category': pCategory, 'price': pPrice, 'color': pColor, 'season': pSeason,
                           'material': pMaterial, 'age': cAge, 'sex': cSex, 'address': cAddress})
        return df

    def saveXML(self, filename):
        # создаем корневой элемент
        data = ET.Element('myShop')
        # создаем таблицу Товары
        products = ET.SubElement(data, 'products')
        # Записываем в нее все товары
        for c in self.products:
            # Добавляем элемент Товар
            prod = ET.SubElement(products, 'products')
            # Добавляем поле к элементу Товар
            id = ET.SubElement(prod, 'id')
            id.text = str(c)
            # Добавляем поле к элементу Товар
            name = ET.SubElement(prod, 'name')
            name.text = self.products[c].name
            # Добавляем поле к элементу Товар
            category = ET.SubElement(prod, 'category_id')
            category.text = str(self.products[c].category)
            # Добавляем поле к элементу Товар
            price = ET.SubElement(prod, 'price')
            price.text = str(self.products[c].price)
            # Добавляем поле к элементу Товар
            color = ET.SubElement(prod, 'color_id')
            color.text = str(self.products[c].color)
            # Добавляем поле к элементу Товар
            size = ET.SubElement(prod, 'size')
            size.text = self.products[c].size
            # Добавляем поле к элементу Товар
            season = ET.SubElement(prod, 'season_id')
            season.text = str(self.products[c].season)
            # Добавляем поле к элементу Товар
            material = ET.SubElement(prod, 'material_id')
            material.text = str(self.products[c].material)
        # Преобразуем в читабельный XML
        md = prettify(data)
        # Записываем в файл
        myfile = open(filename, "w", encoding='utf8')
        myfile.write(md)