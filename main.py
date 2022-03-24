from bd_classes import *

from my_bot import *

from sMenu import Menu

menu_items=["Об авторе", "О программе", "Обучение бота", "Получение рекомендации", "Выход"]
menu_title="Пример меню"

my_menu=Menu(menu_title, menu_items)

choice=0
while choice!=5:
    choice = my_menu.get_user_choice()
    if choice==1:
        pass
    if choice==2:
        pass
    if choice==3:
        shop = my_shop()
        shop.add_sample_data(20)
        shop.add_sample_orders(1000)
        df = shop.getTrainingData()
        df.to_csv("exampleCSV.csv")
        # Создаем бота
        bot = MYBOT(shop)
        # обучаем бота
        bot.botTraining(1)

    if choice==4:
        # получаем данные от пользователя
        sd = bot.getUserChoice()
        # строим рекомендацию и выводим рекомендованный товар
        print("Ваш рекомендованный товар: ", bot.getPrecigion(sd))











