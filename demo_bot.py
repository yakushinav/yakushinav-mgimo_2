from my_shop import MyShop

from myBot import MYBOT


#Создаем магазин товаров
myShop=MyShop("myShop.xml")
#myShop.printProduct()

#Добавляем тестовые данные
myShop.addSampleData(200,2,2)
#myShop.printProduct()
myShop.saveXML("new.xml")

#Создаем бота
bot=MYBOT(myShop)
#обучаем бота
bot.botTraining(1)

#получаем данные от пользователя
sd=bot.getUserChoice()
#строим рекомендацию и выводим рекомендованный товар
print("Ваш рекомендованный товар: ",bot.getPrecigion(sd))