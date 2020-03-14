#подключаем библиотеку
import xml.dom.minidom as minidom

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





