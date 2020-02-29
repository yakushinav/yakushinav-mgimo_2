from sMenu import Menu

menu_items=["Об авторе", "О программе", "Выход"]
menu_title="Пример меню"

my_menu=Menu(menu_title, menu_items)

my_menu.show_menu()
choice=my_menu.get_user_choice()


# TODO: Задание 1. написать обработку для пунктов меню
# TODO: Задание 2. создать меню из пяти пунктов с обработкой
# TODO: Задание 3. создать массив обработчиков пунктов меню
