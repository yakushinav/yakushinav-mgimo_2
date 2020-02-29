#подключаем библиотеку
import xml.dom.minidom as minidom

#читаем XML из файла
dom = minidom.parse("myShop.xml")
dom.normalize()

#Читаем таблицу Materials
pars=dom.getElementsByTagName("material")[0]

#Читаем элементы таблицы Materials
nodes=pars.getElementsByTagName("item")

#Выводим элементы таблицы на экран
for node in nodes:
        id = node.getElementsByTagName("id")[0]
        name = node.getElementsByTagName("name")[0]
        print(id.firstChild.data, name.firstChild.data)

# TODO: Задание 1. добавить чтение остальных таблиц
# TODO: Задание 2. добавить меню для вывода таблицы по запросу пользователя
