import json
import uuid

users = []
user_id = ''
try:
    with open('accounts.txt', "r") as file:
        users = json.load(file)
except FileNotFoundError:
    with open('accounts.txt', "w") as file:
        json.dump(users, file)

def check_account():
    print('Log In/Sign Up')
    name = input('Enter your name: ')
    password = input('Enter your password: ')
    login_result = try_login(name, password)

    if login_result == 1:
        print("Login successful!")
    elif login_result == -1:
        print("Incorrect password.")
        return False
    elif login_result == -2:
        return False
    else:
        print("Creating account...")
        create_account(name, password)

    return True

def try_login(name, password):
    global user_id
    for user in users:
        if user["name"] == name and int(user["failed_login_attempts"]) >= 3:
            return -2
        if user["name"] == name and user["password"] != str(password):
            user["failed_login_attempts"] = str(int(user["failed_login_attempts"]) + 1)
            return -1
        elif user["name"] == name and user["password"] == str(password):
            user_id = user["id"]
            return 1
    print("Account not found.")
    return 0


def create_account(name, password):
    global user_id
    password_confirm = input("Please confirm your password: ")

    if password != password_confirm:
        print("Passwords do not match.")
        create_account(name,password)
        return
    user_id = str(uuid.uuid4())
    user_data = {"id":user_id,"name": name, "password": password, "balance": 0, "transactions": [], "failed_login_attempts": 0}
    users.append(user_data)
    print("User registered successfully!")

def save_and_quit():
    with open('accounts.txt', "w") as file:
        json.dump(users, file)
    print('Thank you for using the ATM!')

def main_menu():
    global users
    print('What would you like to do?')
    print('1. Check balance')
    print('2. Withdraw money')
    print('3. Deposit money')
    print('4. Quit')
    user = users.pop(users.index([user for user in users if user["id"] == user_id][0]))
    balance = float(user["balance"])
    choice = input('Enter your choice: ')

    if choice == '1':
        print('Your balance is $' + str(balance))
        users.append(user)
        main_menu()
    elif choice == '2':
        amount = float(input('Enter the amount to withdraw: '))
        if amount > balance:
            users.append(user)
            print('Insufficient funds.')
        else:
            balance -= amount
            transaction = {"action": "withdraw", "amount": amount, "balance": balance}
            user["transactions"].append(transaction)
            user["balance"] = balance
            users.append(user)
            print('You have withdrawn $' + str(amount) + '. Your balance is $' + str(balance))
        main_menu()
    elif choice == '3':
        amount = float(input('Enter the amount to deposit: '))
        balance += amount
        transaction = {"action": "deposit", "amount": amount, "balance": balance}
        user["transactions"].append(transaction)
        user["balance"] = balance
        users.append(user)
        print('You have deposited $' + str(amount) + '. Your balance is $' + str(balance))
        main_menu()
    elif choice == '4':
        users.append(user)
        save_and_quit()
    else:
        print('Invalid choice. Please try again.')
        main_menu()

print('Welcome to the ATM!')
pin = ''
try_count = 0

while try_count < 3:
    login = check_account()
    if login:
        break
    else:
        try_count += 1


if try_count == 3:
    print('Too many incorrect PIN entries. Your account is now locked.')
else:
    print('Your PIN is correct.')
    main_menu()