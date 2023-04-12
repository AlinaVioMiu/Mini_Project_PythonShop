import pickle
from abc import ABC, abstractmethod
from os.path import exists

from tabulate import tabulate

products = []


class TableRow(ABC):
    @abstractmethod
    def as_row(self):
        pass

    @abstractmethod
    def as_header(self):
        pass


class Product(TableRow):
    def __init__(self, name, price, description='', stock=0):
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock

    def __str__(self) -> str:
        return f'{self.name} price={self.price} stock={self.stock}'

    def __repr__(self):
        return str(self)

    def as_row(self):
        return [self.name, self.price, self.stock, self.description[:min(50, len(self.description))]]

    def as_header(self):
        return ['Name', 'Price', 'Stock', 'Description']


class UserAccount(TableRow):
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password

    def __str__(self) -> str:
        return f'{self.username} - {self.email} - {self.password}'

    def __repr__(self):
        return str(self)

    def as_row(self):
        return [self.username, self.email, self.password]

    def as_header(self):
        return ['Username', 'Email', 'Password']


def save_products():
    with open('products.pickle', 'wb') as file:
        pickle.dump(products, file)  # scrierea efectiva a obiectului in fisier


def load_products():
    if not exists('products.pickle'):
        return list()
    with open('products.pickle', 'rb') as file:
        return pickle.load(file)  # citirea efectiva a obiectului din fisier


def save_users(users):
    with open('users.pickle', 'wb') as file:
        pickle.dump(users, file)  # scrierea efectiva a obiectului in fisier


def read_users():
    if not exists('users.pickle'):
        return list()
    with open('users.pickle', 'rb') as file:
        return pickle.load(file)


def register_user():
    print('Creare cont utilizator:')
    try:
        username = input('username = ')
        if len(username) == 0:
            raise ValueError
        password = input('password= ')
        if len(password) == 0:
            raise ValueError
        email = input('email= ')
        if len(email) == 0:
            raise ValueError
        user = UserAccount(username, password, email)
        users_ = read_users()
        users_.append(user)
        save_users(users_)
        print('User creat cu succes!')
    except ValueError:
        print('Value Error! Introduceti o valoare valida!')


def login_user():
    print('Autentificare utilizator:')
    username = input('username = ')
    password = input('password= ')
    users = read_users()
    for user in users:
        if user.username == username and user.password == password:
            return True
        print('Autentificare reusita!')
    else:
        print('User sau parola gresita!')
        return False


def print_menu():
    menu = ['Iesire', 'Adaugare produs', 'Listare produse', 'Cumparare produs', 'Modificare produs',
            'Stergere produs', 'Listare useri', 'Login user', 'Register user']
    # header = ['Nr.crt', 'Menu']
    for index, value in enumerate(menu):
        print(index, value, sep='. ')


def select_product():
    table(products)
    choice = int(input('Alegeti un produs: '))
    return products[choice]


def sell_product():
    product = select_product()
    quantity = int(input('Alegeti cantitatea: '))
    print('Produs vandut!')
    print(f'Aveti de achitat suma de {product.price * quantity} lei')
    product.stock -= quantity
    save_products()


def add_product():
    try:
        name = input('name=')
        if len(name) == 0:
            raise ValueError
        price = float(input('price='))
        if price <= 0:
            raise ValueError
        description = input('description=')
        stock = int(input('stock='))
        product = Product(name, price, description, stock)
        products.append(product)
        save_products()
        print('Produs adaugat!')
        print('-----------------------')
    except ValueError:
        print('Value Error! Ar trebui introdusa o valoare valida de la tastatura!')


def table(items):
    tabel = []
    for item in items:
        header = item.as_header()
        tabel.append(item.as_row())
    print(tabulate(tabel, header, showindex='always', tablefmt='fancy_grid'))


# def list_items(items):
#     for product in products:
#         print(f'|{product.name:<25}|{product.price:^25}|{product.stock:>25}|')


def interpret_command(command):
    match command:
        case '1':
            add_product()
        case '2':
            table(products)
        case '3':
            sell_product()
        case '4':
            modify_product()
        case '5':
            delete_product()
        case '6':
            table(read_users())
        case '7':
            login_user()
        case '8':
            register_user()


def delete_product():
    product = select_product()
    products.remove(product)
    save_products()
    print('Produs sters!')
    print('---------------------------------')


def modify_product():
    product = select_product()
    print(f'Efectuati modificarile: ')
    try:
        name = input(f'name (currently "{product.name}", press enter to keep) = ')
        if len(name) > 0:
            product.name = name
        price = input(f'price (currently "{product.price}", press enter to keep) = ')
        if price != '':
            product.price = float(price)
        description = input(f'description (currently "{product.description}", press enter to keep) = ')
        if description != '':
            product.description = description
        stock = input(f'stock (currently "{product.stock}", press enter to keep) = ')
        if stock != '':
            product.stock = int(stock)
        print('Produs modificat!')
        print('-----------------------------------')
    except ValueError:
        print('Value Error! Ar trebui introdusa o valoare valida de la tastatura!')
    save_products()


products = load_products()
print_menu()
command = input('Introduceti o comanda: ')
while command != '0':
    interpret_command(command)
    print_menu()
    command = input('Introduceti o comanda: ')
