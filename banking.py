# Write your code here
import random
import sqlite3
conn = sqlite3.connect('card.s3db')
# conn = sqlite3.connect(r"D:\andrew\sqlite\db\card.s3db")
cur = conn.cursor()
# cur.execute('CREATE DATABASE IF NOT EXISTS card')
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()


def card_number_checksum(number):
    mass = [int(x) for x in str(number)]
    for x in range(0, 16, 2):
        mass[x] = mass[x] * 2
        if mass[x] > 9:
            mass[x] = mass[x] - 9
    s = sum(mass)
    if s % 10 == 0:
        return 0
    else:
        return 10 - s % 10


def check_card(number):
    # print(number[:-1], card_number_checksum(number[:-1]), number[-1:])
    if card_number_checksum(number[:-1]) == int(number[-1:]):
        cur.execute(f'SELECT * from card WHERE number={number}')
        db = cur.fetchall()
        if db:
            return True
        else:
            print("Such a card does not exist.")
            return False
    else:
        print("Probably you made mistake in the card number.")
        print("Please try again!")
        return False


def transfer_to(dest, money):
    # print(dest, money)
    cur.execute(f'SELECT balance FROM card WHERE number={dest}')
    db = cur.fetchone()
    dest_balance = db[0]
    dest_balance += money
    cur.execute(f'UPDATE card SET balance={dest_balance} WHERE number={dest}')
    conn.commit()
    return


def fetch_all_accounts():
    cur.execute('SELECT id FROM card')
    db = cur.fetchall()
    conn.commit()
    return {i[0] for i in db}


class CreditCard:

    def __init__(self):
        self.account = 0
        self.pin = '0000'
        self.card_number = '4000000000000000'
        self.balance = 0
        self.menu()

    def menu(self):
        # cur.execute('SELECT * from card')
        # db = cur.fetchall()
        # conn.commit()
        # print(db)
        # print(fetch_all_accounts())
        print()
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        action = input()
        if action == '1':
            self.create()
        elif action == '2':
            self.login()
        elif action == '0':
            print("Bye!")
            conn.close()
            exit()
        else:
            self.menu()

    def create(self):
        accounts = fetch_all_accounts()
        # print(accounts)
        while self.account == 0 or self.account in accounts:
            self.account = random.randint(1, 999999999)
        self.pin = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
        self.card_number = str(400000000000000 + self.account) + str(
                card_number_checksum(400000000000000 + self.account))
        cur.execute(f'INSERT INTO card VALUES ({self.account}, {self.card_number}, {self.pin}, 0);')
        conn.commit()
        # accounts = fetch_all_accounts()
        # print(accounts)
        print("Your card has been created")
        print("Your card number:")
        print(self.card_number)
        print("Your card PIN:")
        print(self.pin)
        self.menu()

    def login(self):
        print()
        print("Enter your card number:")
        in_card_number = input()
        print("Enter your PIN:")
        in_pin = input()
        cur.execute(f'SELECT * from card WHERE number = {in_card_number}')
        db = cur.fetchone()
        # print(db)
        if db:
            if in_pin == db[2]:
                self.account = db[0]
                self.card_number = db[1]
                self.pin = db[2]
                self.balance = db[3]
                print("You have successfully logged in!")
                self.account_menu()
            else:
                print("Wrong card number or PIN")
        else:
            print("Wrong card number or PIN")
        self.menu()

    def account_menu(self):
        print()
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        action = input()
        if action == '1':
            self.show_balance()
        elif action == '2':
            self.add_income()
        elif action == '3':
            self.do_transfer()
        elif action == '4':
            self.close_account()
        elif action == '5':
            print("You have successfully logged out!")
            self.menu()
        elif action == '0':
            print("Bye!")
            conn.close()
            exit()

    def show_balance(self):
        print("Balance", self.balance)
        self.account_menu()

    def add_income(self):
        print()
        print("Enter income:")
        income = int(input())
        self.balance += income
        cur.execute(f'UPDATE card SET balance={self.balance} WHERE number={self.card_number}')
        conn.commit()
        print("Income was added!")
        self.account_menu()

    def do_transfer(self):
        print()
        print("Transfer")
        print("Enter card number:")
        in_number = input()
        if in_number == self.card_number:
            print("You can't transfer money to the same account!")
        else:
            if check_card(in_number):
                print("Enter how much money you want to transfer:")
                wants = int(input())
                if self.balance > wants:
                    self.balance -= wants
                    cur.execute(f'UPDATE card SET balance={self.balance} WHERE number={self.card_number}')
                    conn.commit()
                    transfer_to(in_number, wants)
                    print("Success!")
                else:
                    print("Not enough money!")
        self.account_menu()

    def close_account(self):
        cur.execute(f'DELETE from card WHERE number={self.card_number}')
        conn.commit()
        self.menu()


# cur.execute('CREATE TABLE card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
# cur.execute('INSERT INTO card VALUES (0, 4000000000000000, "0000", 0);')
# conn.commit()
# print(fetch_all_accounts())
client = CreditCard()
# cur.execute('INSERT INTO card VALUES (0, 4000000000000000, "0000", 0);')
# cur.execute('DELETE FROM card WHERE number="4000009828882012"')
# print(cur.lastrowid)
# conn.commit()


# print(cur.fetchall())
