class Menu:
    def __init__(self, title,items):
        self.title = title
        self.items = list()
        for item in items:
            self.items.append(item)

    def show_menu(self):

        print("-- ", self.title, " --")

        item_number = 1
        for item in self.items:
            print("[{}] - {}".format(item_number,item))
            item_number += 1

    def get_user_choice(self):
        self.show_menu()
        flag=0
        while flag==0:
            user_input = int(input("Ваш выбор> "))
            if ((user_input>=1)and (user_input<=len(self.items))):
                flag=1
            else:
                print("Неверный ввод")

        return user_input